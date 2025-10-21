#ifndef SPI_DISPLAY_H
#define SPI_DISPLAY_H

#include <stdint.h>
#include <stdbool.h>
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


static spi_display_t display;

/**
 * SPI initialization callback for ST7789 driver
 */
static uint8_t st7789_spi_init_callback(void);

/**
 * SPI deinitialization callback for ST7789 driver
 */
static uint8_t st7789_spi_deinit_callback(void);

/**
 * SPI write callback for ST7789 driver
 * 
 * @param buf: byte array message to send
 * @param len: length of buffer
 */
static uint8_t st7789_spi_write_callback(uint8_t *buf, uint16_t len);

/**
 * Command/Data GPIO init callback
 */
static uint8_t st7789_cmd_data_gpio_init_callback(void);

/**
 * Command/Data GPIO deinit callback
 */
static uint8_t st7789_cmd_data_gpio_deinit_callback(void);

/**
 * Command/Data GPIO write callback
 */
static uint8_t st7789_cmd_data_gpio_write_callback(uint8_t data);

/**
 * Reset GPIO init callback
 */
static uint8_t st7789_reset_gpio_init_callback(void);

/**
 * Reset GPIO deinit callback
 */
static uint8_t st7789_reset_gpio_deinit_callback(void);

/**
 * Reset GPIO write callback
 */
static uint8_t st7789_reset_gpio_write_callback(uint8_t data);

/**
 * Delay callback
 */
static void st7789_delay_ms_callback(uint32_t ms);

/**
 * Debug print callback
 */
static void st7789_debug_print_callback(const char *fmt, ...);

/**
 * Checks for any pin assignment conflict
 * 
 * @param pins: array of pins to validate
 * @param spi0_idx: flag to use default spi0 pins or spi1
 * 
 * @return true if pins are valid, false otherwise 
 */
bool is_valid_pin_assignment (int8_t *pins, bool spi0_idx);

/**
 * Initialize st7789 display handle by setting all
 * the callback functions
 * 
 * @param g_st7789_handle: st7789 display handle
 */
void handle_init (st7789_handle_t *g_st7789_handle);

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
display_err_t display_init(bool spi0_idx, int8_t reset_pin, int8_t data_cmd_pin, int8_t backlight_pin, st7789_handle_t *g_st7789_handle);

#endif