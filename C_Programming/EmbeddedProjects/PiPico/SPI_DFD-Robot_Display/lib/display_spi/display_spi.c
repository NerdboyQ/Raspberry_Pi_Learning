#include "pico/stdlib.h"
#include "hardware/spi.h"
#include <stdint.h>
#include "driver_st7789.h"
#include "display_spi.h"

// changing to global source singleton 
spi_display_t display;

/**
 * SPI initialization callback for ST7789 driver
 */
uint8_t st7789_spi_init_callback(void) {
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
uint8_t st7789_spi_deinit_callback(void) {
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
uint8_t st7789_spi_write_callback(uint8_t *buf, uint16_t len) {
    gpio_put(display.spi_pin_cs, 0); // Select chip
    if (!display.spi_index) spi_write_blocking(spi0, buf, len);
    else spi_write_blocking(spi1, buf, len);
    gpio_put(display.spi_pin_cs, 1); // Deselect chip
    return 0;
}

/**
 * Command/Data GPIO init callback
 */
uint8_t st7789_cmd_data_gpio_init_callback(void) {
    gpio_init(display.display_pin_dc);
    gpio_set_dir(display.display_pin_dc, GPIO_OUT);
    return 0;
}

/**
 * Command/Data GPIO deinit callback
 */
uint8_t st7789_cmd_data_gpio_deinit_callback(void) {
    // Nothing special needed
    return 0;
}

/**
 * Command/Data GPIO write callback
 */
uint8_t st7789_cmd_data_gpio_write_callback(uint8_t data) {
    gpio_put(display.display_pin_dc, data);
    return 0;
}

/**
 * Reset GPIO init callback
 */
uint8_t st7789_reset_gpio_init_callback(void) {
    gpio_init(display.display_pin_rt);
    gpio_set_dir(display.display_pin_rt, GPIO_OUT);
    return 0;
}

/**
 * Reset GPIO deinit callback
 */
uint8_t st7789_reset_gpio_deinit_callback(void) {
    // Nothing special needed
    return 0;
}

/**
 * Reset GPIO write callback
 */
uint8_t st7789_reset_gpio_write_callback(uint8_t data) {
    gpio_put(display.display_pin_rt, data);
    return 0;
}

/**
 * Delay callback
 */
void st7789_delay_ms_callback(uint32_t ms) {
    sleep_ms(ms);
}

/**
 * Debug print callback
 */
void st7789_debug_print_callback(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}

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

// END --- ST7789 SPI callback functions =============================================================