/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/dma.h"
#include <stdlib.h>

#include "driver_st7789.h"

// Common ST7789 pin definitions for Pico
// Adjust these to match your wiring
#define DFLT_PIN_DC   0 // GPIO0 - DC pin //20  // Data/Command
#define DFLT_PIN_RST  1 // GPIO1 - RT pin //21  // Reset
#define DFLT_PIN_SCK  2 // GPIO2 SPI0 SCK // 18
#define DFLT_PIN_MOSI 3 // GPIO3 SPI0 Tx  // 19
#define DFLT_PIN_MISO 4 // GPIO4 SPI0 Rx  // 16
#define DFLT_PIN_CS   5 // GPIO5 SPI0 CSn // 17
#define DFLT_SPI_PORT spi0

#if 0 
    #define PIN_BL   22  // Backlight (optional)
#endif

// Pico W devices use a GPIO on the WIFI chip for the LED,
// so when building for Pico W, CYW43_WL_GPIO_LED_PIN will be defined
#ifdef CYW43_WL_GPIO_LED_PIN
#include "pico/cyw43_arch.h"
#endif

#ifndef LED_DELAY_MS
#define LED_DELAY_MS 150
#endif

// Perform initialization
int pico_led_init(void) {
#if defined(PICO_DEFAULT_LED_PIN)
    // A device like Pico that uses a GPIO for the LED will define PICO_DEFAULT_LED_PIN
    // so we can use normal GPIO functionality to turn the led on and off
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    return PICO_OK;
#elif defined(CYW43_WL_GPIO_LED_PIN)
    // For Pico W devices we need to initialise the driver etc
    return cyw43_arch_init();
#endif
}

// Turn the led on or off
void pico_set_led(bool led_on) {
#if defined(PICO_DEFAULT_LED_PIN)
    // Just set the GPIO on or off
    gpio_put(PICO_DEFAULT_LED_PIN, led_on);
#elif defined(CYW43_WL_GPIO_LED_PIN)
    // Ask the wifi "driver" to set the GPIO on or off
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
#endif
}

#include <pthread.h>


// Dimensions of the sprite
#define MEGAMAN_WIDTH  32
#define MEGAMAN_HEIGHT 32

// RGB565 Colors (example definitions)
// RRRRR GGGGGG BBBBB
// Demo 16bit RGB sprite 
uint16_t demo_green_hair_sprite[MEGAMAN_WIDTH * MEGAMAN_HEIGHT] = {
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x2b25, 0x2b25, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x2b25, 0x2b25, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x2b25, 0x2b25, 0x5649, 0x5e69, 0x5e69, 0x5649, 0x2b25, 0x2b25, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x2263, 0x2263, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x2263, 0x2263, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x2243, 0x2263, 0x5669, 0x5e69, 0x5e69, 0x5669, 0x2263, 0x2243, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0x5669, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x5669, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0xe4ce, 0xe4ce, 0x44c7, 0x44c7, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x44c7, 0x44c7, 0xe4ce, 0xe4ce, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x49a4, 0x4984, 0xe4ce, 0xe4ce, 0x44c7, 0x44c7, 0x5e69, 0x5e69, 0x5e69, 0x5e69, 0x44c7, 0x44c7, 0xe4ce, 0xe4ce, 0x4984, 0x49a4, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x44c7, 0x44c7, 0x44c7, 0x44c7, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x44c7, 0x44c7, 0x44c7, 0x44c7, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0x6226, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x6226, 0x6226, 0xfdf3, 0xfdf3, 0x9a68, 0x9a68, 0xfdf3, 0xfdf3, 0x0000, 0x0000, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x0000, 0x0000, 0xfdf3, 0xfdf3, 0x9a68, 0x9a68, 0xfdf3, 0xfdf3, 0x6226, 0x6226, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x6226, 0x6226, 0xfdf3, 0xfdf3, 0x9a68, 0x9a68, 0xfdf3, 0xfdf3, 0x0000, 0x0000, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x0000, 0x0000, 0xfdf3, 0xfdf3, 0x9a68, 0x9a68, 0xfdf3, 0xfdf3, 0x6226, 0x6226, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0xe36b, 0xe36b, 0xe4ce, 0xe4ce, 0x0000, 0x0000, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x0000, 0x0000, 0xe4ce, 0xe4ce, 0xe36b, 0xe36b, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0xe36b, 0xe36b, 0xe4ce, 0xe4ce, 0x0000, 0x0000, 0xfdf3, 0xfdf3, 0xfdf3, 0xfdf3, 0x0000, 0x0000, 0xe4ce, 0xe4ce, 0xe36b, 0xe36b, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4984, 0x4984, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0x4984, 0x4984, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x01a9, 0x01a9, 0x94aa, 0x94aa, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x94aa, 0x94aa, 0x4841, 0x4841, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x01a9, 0x01a9, 0x94aa, 0x94aa, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x4984, 0x94aa, 0x94aa, 0x4841, 0x4841, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x01a9, 0x01a9, 0x0333, 0x0333, 0xc62d, 0xc62d, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xc62d, 0xc62d, 0x98a2, 0x98a2, 0x4841, 0x4841, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x01a9, 0x0189, 0x0333, 0x0333, 0xc62d, 0xc62d, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xe4ce, 0xc62d, 0xc62d, 0x98a2, 0x98a2, 0x4841, 0x4841, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x022c, 0x022c, 0x0c59, 0x0c59, 0x0c59, 0x0c59, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc8e3, 0xc8e3, 0xc8e3, 0xc8e3, 0x6061, 0x6061, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x022c, 0x022c, 0x0c59, 0x0c59, 0x0c59, 0x0c59, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc62d, 0xc8e3, 0xc8e3, 0xc8e3, 0xc8e3, 0x6061, 0x6061, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x022c, 0x022c, 0x0d7f, 0x0d7f, 0x0c59, 0x0c59, 0x022c, 0x022c, 0xc62d, 0xc62d, 0x239b, 0x239c, 0x239b, 0x239b, 0xc62d, 0xc62d, 0x6061, 0x6061, 0xc8e3, 0xc8e3, 0xf904, 0xf904, 0x6061, 0x6061, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x022c, 0x022c, 0x0d7f, 0x0d7f, 0x0c59, 0x0c59, 0x022c, 0x022c, 0xc62d, 0xc62d, 0x239b, 0x239b, 0x239b, 0x239b, 0xc62d, 0xc62d, 0x6061, 0x6061, 0xc8e3, 0xc8e3, 0xf904, 0xf904, 0x6061, 0x6061, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x022c, 0x022c, 0x022c, 0x022c, 0xf904, 0xf904, 0xf904, 0xf904, 0xf904, 0xf904, 0x0d7f, 0x0d7f, 0x0d7f, 0x0d7f, 0x0d7f, 0x0d7f, 0x6061, 0x6061, 0x6061, 0x6061, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x022c, 0x022c, 0x022c, 0x022c, 0xf904, 0xf904, 0xf904, 0xf904, 0xf904, 0xf904, 0x0d7f, 0x0d5f, 0x0d7f, 0x0d7f, 0x0d7f, 0x0d7f, 0x6061, 0x6061, 0x6061, 0x6061, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x6061, 0x6061, 0xf904, 0xf904, 0xf904, 0xf924, 0xc8c3, 0xc8c3, 0x0c59, 0x0c59, 0x0d7f, 0x0d7f, 0x0d5f, 0x0d7f, 0x022c, 0x022c, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x6061, 0x6061, 0xf904, 0xf904, 0xf904, 0xf904, 0xc8c3, 0xc8c3, 0x0c59, 0x0c59, 0x0d7f, 0x0d7f, 0x0d7f, 0x0d7f, 0x022c, 0x022c, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4841, 0x4841, 0xc8c3, 0xc8c3, 0xc8c3, 0xc8c3, 0x6061, 0x6061, 0x022c, 0x022c, 0x0c59, 0x0c59, 0x0c59, 0x0c59, 0x01a9, 0x01a9, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4841, 0x4841, 0xc8c3, 0xc8c3, 0xc8c3, 0xc8c3, 0x6061, 0x6061, 0x022c, 0x022c, 0x0c59, 0x0c59, 0x0c59, 0x0c59, 0x01a9, 0x01a9, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4841, 0x4841, 0x4841, 0x4841, 0x0000, 0x0000, 0x0000, 0x0000, 0x01a9, 0x01a9, 0x01a9, 0x01a9, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 
  0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4841, 0x4841, 0x4841, 0x4841, 0x0000, 0x0000, 0x0000, 0x0000, 0x01a9, 0x01a9, 0x01a9, 0x01a9, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000
};


#define SPI_BAUD_RATE 10 * 1000 * 1000 // 10 MHz

/**
 * Display Errors Status enum
 */
typedef enum {
    displaySts_success = 0,
    displaySts_fail_init = 1,
    displaySts_fail_comm = 2,
    displaySts_fail_alloc = 3,
    displaySts_fail_param = 4
} display_err_t;

/**
 * SPI display Data Structure for pins
 */
typedef struct {
    uint8_t spi_index;
    uint8_t spi_pin_cs, spi_pin_miso, spi_pin_mosi, spi_pin_clk;
    uint8_t display_pin_rt, display_pin_dc, display_pin_bl;
} spi_display_t;


spi_display_t display;

// START --- ST7789 SPI callback functions =============================================================

/**
 * SPI initialization callback for ST7789 driver
 */
static uint8_t st7789_spi_init_callback(void) {
    // Initialize SPI
    // spi_init(spi0, 62500000); // 62.5 MHz
    spi_init(spi0, 1000*1000);
    gpio_set_function(display.spi_pin_miso, GPIO_FUNC_SPI);
    gpio_set_function(display.spi_pin_clk, GPIO_FUNC_SPI);
    gpio_set_function(display.spi_pin_mosi, GPIO_FUNC_SPI);
    
    // Chip select is active-low
    gpio_init(display.spi_pin_cs);
    gpio_set_dir(display.spi_pin_cs, GPIO_OUT);
    gpio_put(display.spi_pin_cs, 1);
    
    return 0;
}

/**
 * SPI deinitialization callback for ST7789 driver
 */
static uint8_t st7789_spi_deinit_callback(void) {
    if (!display.spi_index) spi_deinit(spi0);
    else  spi_deinit(spi1);
    return 0;
}

/**
 * SPI write callback for ST7789 driver
 * 
 * @param buf: byte array message to send
 * @param len: length of buffer
 */
static uint8_t st7789_spi_write_callback(uint8_t *buf, uint16_t len) {
    gpio_put(display.spi_pin_cs, 0); // Select chip
    if (!display.spi_index) spi_write_blocking(spi0, buf, len);
    else spi_write_blocking(spi1, buf, len);
    gpio_put(display.spi_pin_cs, 1); // Deselect chip
    return 0;
}

/**
 * Command/Data GPIO init callback
 */
static uint8_t st7789_cmd_data_gpio_init_callback(void) {
    gpio_init(display.display_pin_dc);
    gpio_set_dir(display.display_pin_dc, GPIO_OUT);
    return 0;
}

/**
 * Command/Data GPIO deinit callback
 */
static uint8_t st7789_cmd_data_gpio_deinit_callback(void) {
    // Nothing special needed
    return 0;
}

/**
 * Command/Data GPIO write callback
 */
static uint8_t st7789_cmd_data_gpio_write_callback(uint8_t data) {
    gpio_put(display.display_pin_dc, data);
    return 0;
}

/**
 * Reset GPIO init callback
 */
static uint8_t st7789_reset_gpio_init_callback(void) {
    gpio_init(display.display_pin_rt);
    gpio_set_dir(display.display_pin_rt, GPIO_OUT);
    return 0;
}

/**
 * Reset GPIO deinit callback
 */
static uint8_t st7789_reset_gpio_deinit_callback(void) {
    // Nothing special needed
    return 0;
}

/**
 * Reset GPIO write callback
 */
static uint8_t st7789_reset_gpio_write_callback(uint8_t data) {
    gpio_put(display.display_pin_rt, data);
    return 0;
}

/**
 * Delay callback
 */
static void st7789_delay_ms_callback(uint32_t ms) {
    sleep_ms(ms);
}

/**
 * Debug print callback
 */
static void st7789_debug_print_callback(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}

// END --- ST7789 SPI callback functions =============================================================

/**
 * Checks for any pin assignment conflict
 * 
 * @param pins: array of pins to validate
 * @param spi0_idx: flag to use default spi0 pins or spi1
 * 
 * @return true if pins are valid, false otherwise 
 */
bool is_valid_pin_assignment (int8_t *pins, bool spi0_idx) {
    // check if pin assignment is within valid pin range for pi pico
    if (pins[0] < 0 || pins[0] > 28) return false; // reset pin
    if (pins[1] < 0 || pins[1] > 28) return false; // data cmd pin
    if (pins[2] > 28) return false; // backlight pin

    int8_t spi_pin_l = 2;
    int8_t spi_pin_h = 5;
    if (!spi0_idx) {
        spi_pin_l = 10;
        spi_pin_h = 13;
    }

    for (int i = 0; i < 3; i++) {
        if (pins[i] < 0) continue; // ignore invalid values
        if (pins[i] == pins[(i+1)%3] || pins[i] == pins[(i+2)%3]) return false;
        if (pins[i] >= spi_pin_l && pins[i] <= spi_pin_h) return false;
    }

    return true;
}

/**
 * Initialize st7789 display handle by setting all
 * the callback functions
 * 
 * @param g_st7789_handle: st7789 display handle
 */
void handle_init (st7789_handle_t *g_st7789_handle) {
    // Link callback functions
    g_st7789_handle->spi_init = st7789_spi_init_callback;
    g_st7789_handle->spi_deinit = st7789_spi_deinit_callback;
    g_st7789_handle->spi_write_cmd = st7789_spi_write_callback;
    g_st7789_handle->cmd_data_gpio_init = st7789_cmd_data_gpio_init_callback;
    g_st7789_handle->cmd_data_gpio_deinit = st7789_cmd_data_gpio_deinit_callback;
    g_st7789_handle->cmd_data_gpio_write = st7789_cmd_data_gpio_write_callback;
    g_st7789_handle->reset_gpio_init = st7789_reset_gpio_init_callback;
    g_st7789_handle->reset_gpio_deinit = st7789_reset_gpio_deinit_callback;
    g_st7789_handle->reset_gpio_write = st7789_reset_gpio_write_callback;
    g_st7789_handle->delay_ms = st7789_delay_ms_callback;
    g_st7789_handle->debug_print = st7789_debug_print_callback;
}

/**
 * Initializes the spi display
 * 
 * @param spi0_idx: default spi0 idx
 * @param reset_pin: target display reset pin
 * @param data_cmd_pin: target display Data Command pin
 * @param reset_pin: target display backlight pin
 * @param g_st7789_handle: st7789 display handle
 * 
 * @return display_init error status
 */
display_err_t display_init(bool spi0_idx, int8_t reset_pin, int8_t data_cmd_pin, int8_t backlight_pin, st7789_handle_t *g_st7789_handle) {

    int8_t pins[3] = {
        reset_pin,
        data_cmd_pin,
        backlight_pin
    };
    
    // check for valid pin assignment
    if (!is_valid_pin_assignment(pins, spi0_idx)) return displaySts_fail_param;

    display.display_pin_rt = reset_pin;
    display.display_pin_dc = data_cmd_pin;

    // Optional: Backlight
    if (backlight_pin > -1) {
        display.display_pin_bl = backlight_pin;
        gpio_init(display.display_pin_bl);
        gpio_set_dir(display.display_pin_bl, GPIO_OUT);
        gpio_put(display.display_pin_bl, 1); // Turn on backlight
    }

    /** 
     * Use default pins to avoid confusion
     * 
     * spi0:
     * GPIO pins  2-5
     * 
     * spi1:
     * GPIO pins 10-13
     */
    if (spi0_idx) {
        spi_init(spi0, SPI_BAUD_RATE);
        display.spi_pin_clk = DFLT_PIN_SCK;
        display.spi_pin_cs = DFLT_PIN_CS;
        display.spi_pin_mosi = DFLT_PIN_MOSI;
        display.spi_pin_miso = DFLT_PIN_MISO;
    } else {
        spi_init(spi1, SPI_BAUD_RATE);
        display.spi_pin_clk = DFLT_PIN_SCK+8;
        display.spi_pin_cs = DFLT_PIN_CS+8;
        display.spi_pin_mosi = DFLT_PIN_MOSI+8;
        display.spi_pin_miso = DFLT_PIN_MISO+8;
    }

    // initialize all st7789 callback functions
    handle_init(g_st7789_handle);
    
    printf("Initializing ST7789...\n");
    
    // Initialize the display
    uint8_t res = st7789_init(g_st7789_handle);
    // check initializtion status
    if (res) {
        printf("!ERROR: st7789 init failed: %d\n", res);
        return displaySts_fail_init;
    }

    // Set display dimensions (240x320 typical for ST7789)
    st7789_set_column(g_st7789_handle, 240);
    st7789_set_row(g_st7789_handle, 320);
    
    // Wake up display
    res = st7789_sleep_out(g_st7789_handle);
    if (res != 0) {
        printf("Sleep out failed: %d\n", res);
        return displaySts_fail_init;
    }
    
    // Set pixel format to RGB565
    res = st7789_set_interface_pixel_format(g_st7789_handle, 
                                            ST7789_RGB_INTERFACE_COLOR_FORMAT_65K,
                                            ST7789_CONTROL_INTERFACE_COLOR_FORMAT_16_BIT);
    if (res != 0) {
        printf("Set pixel format failed: %d\n", res);
        return displaySts_fail_init;
    }
    
    // inverting the pixels RGB encoding to avoid constantly inverting colors at runtime
    res = st7789_display_inversion_on(g_st7789_handle);
    if (res != 0) {
        printf("Display inversion on failed: %d\n", res);
        return displaySts_fail_init;
    }

    // Turn on display
    res = st7789_display_on(g_st7789_handle);
    if (res != 0) {
        printf("Display on failed: %d\n", res);
        return displaySts_fail_init;
    }

    printf("Display initialized!\n");
    
    return displaySts_success;
}

/**
 * Simple function to test basic st7789 initialization of color display
 * 
 * @return false if no issue occurs with the test, otherwise return true
 */
bool test_spi_display() {
    // Initialize st7789 handle & display data structure
    static st7789_handle_t g_st7789_handle;
    static bool initialized = false;

    // Only initialize once
    if (!initialized) {
        printf("Intializing display\n");
        display_err_t init_status = display_init(true, DFLT_PIN_RST, DFLT_PIN_DC, -1, &g_st7789_handle);
        if (init_status) {
            printf(" !ERROR: failure %d: ", init_status);
            switch (init_status) {
                case displaySts_fail_alloc:
                    printf("FAILED MEMORY ALLOCATION\n");
                    break;
                case displaySts_fail_comm:
                    printf("FAILED COMMUNICATION\n");
                    break;
                case displaySts_fail_init:
                    printf("FAILED INIT\n");
                    break;
                case displaySts_fail_param:
                    printf("BAD PARAMS\n");
                    break;
                    
                default:
                    printf("UNKNOWN ERROR\n");
                    break;
            }
            return true;
        }

        initialized = true;
    }

    printf("Starting tests...\n\n");

    // Clear screen
    printf("Clearing screen...\n");
    st7789_clear(&g_st7789_handle);
    sleep_ms(1000);
    
    /**
     * The DFD Robot 240x320 display uses the st7789. It is a 16bit color display 
     * w/ the RGB 565 color encoding:
     * 
     *      0000|0 000|000 0|0000
     * Full Red  :  0xF800 (upper  5 bits)
     * Full Green:  0x07E0 (center 6 bits)
     * Full Blue :  0x001F (lower  5 bits)
     */
    // printf("Test 1: Red rectangle\n");
    // st7789_fill_rect(&g_st7789_handle, 10, 10, 110, 110, 0xf800);
    // sleep_ms(2000);
    
    // Test 2: Green rectangle
    // printf("Test 2: Green rectangle\n");
    // st7789_fill_rect(&g_st7789_handle, 130, 10, 230, 110, 0x07E0);
    // sleep_ms(2000);
    
    // Test 3: Blue rectangle
    // printf("Test 3: Blue rectangle\n");
    // st7789_fill_rect(&g_st7789_handle, 10, 140, 110, 240, 0x001F);
    // sleep_ms(2000);

    // Test 4: Gray rectangle
    // printf("Test 4: Grey rectangle\n");
    // st7789_fill_rect(&g_st7789_handle, 130, 140, 230, 240, 0x8410);
    // sleep_ms(2000);

    // printf("Test: All bits on (0xFFFF - should be white)\n");
    // st7789_fill_rect(&g_st7789_handle, 0, 240, 239, 319, 0xFFFF);
    // sleep_ms(3000);

    // Test combinations
    // printf("Test: Red + Green (0xF7E0 - should be yellow)\n");
    // st7789_fill_rect(&g_st7789_handle, 0, 0, 119, 159, 0xFFE0);
    // sleep_ms(3000);

    // printf("Test: Red + Blue (0xF81F - should be magenta)\n");
    // st7789_fill_rect(&g_st7789_handle, 120, 0, 239, 159, 0xF81F);
    // sleep_ms(3000);

    // printf("Test: Green + Blue (0x07FF - should be cyan)\n");
    // st7789_fill_rect(&g_st7789_handle, 0, 160, 119, 319, 0x07FF);

    uint16_t left, top;
    left = 10;
    top = 10;
    // the offsets need to be the height & width of the image, inclusive to the starting pixel column/row
    st7789_draw_picture_16bits(&g_st7789_handle,left, top, left+31, top +31, demo_green_hair_sprite);
    
    sleep_ms(6000);


    printf("All tests complete!\n");

    return false;
}


int main() {
    
    sleep_ms(4000);
    stdio_init_all(); // initialize I/O GPIO pins
    int rc = pico_led_init(); // intialize pico w specific led pin
    hard_assert(rc == PICO_OK);
    
    while (true) {
        pico_set_led(true);
        sleep_ms(LED_DELAY_MS);
        pico_set_led(false);
        sleep_ms(LED_DELAY_MS);
        // test display
        test_spi_display();
    }

    return 0;
}