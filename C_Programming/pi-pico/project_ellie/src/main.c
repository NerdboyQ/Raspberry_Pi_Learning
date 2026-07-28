/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

// #include <stdio.h>

#include "DFRobot_RGBPanel/DFRobot_RGBPanel.h"

// SPI Defines
// We are going to use SPI 0, and allocate it to the following GPIO pins
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define SPI_PORT spi0
#define PIN_MISO (4)
#define PIN_CS   (5)
#define PIN_SCK  (2)
#define PIN_MOSI (3)

// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define I2C_PORT i2c0
#define I2C_SDA (8)
#define I2C_SCL (9)

DFRobot_RGBPanel_t rgb_panel;

/**
 * Initializes the SPI interface at 1MHz, and configure
 * the GPIO pins for SPI use.
 */
void init_spi() {
    // Initialise SPI at 1MHz
    spi_init(SPI_PORT, 1000*1000);
    gpio_set_function(PIN_MISO, GPIO_FUNC_SPI);
    gpio_set_function(PIN_CS,   GPIO_FUNC_SIO);
    gpio_set_function(PIN_SCK,  GPIO_FUNC_SPI);
    gpio_set_function(PIN_MOSI, GPIO_FUNC_SPI);
    
    // Chip select is active-low, so we'll initialise it to a driven-high state
    gpio_set_dir(PIN_CS, GPIO_OUT);
    gpio_put(PIN_CS, 1);
}

/**
 * Initializes the I2C interface at 400KHz, and configure
 * the GPIO pins for I2C use.
 */
void init_i2c() {
    // Initialise I2C at 400KHz
    i2c_init(I2C_PORT, 400*1000);
    
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);
}

void scan_i2c_bus() {
    printf("\n--- Scanning I2C Bus on GPIO 8/9 ---\n");
    int count = 0;
    for (uint8_t addr = 0x08; addr < 0x78; addr++) {
        uint8_t rx;
        // Perform a 1-byte read test
        int ret = i2c_read_blocking(I2C_PORT, addr, &rx, 1, false);
        if (ret >= 0) {
            printf(" -> Found device at address: 0x%02X\n", addr);
            count++;
        }
    }
    if (count == 0) {
        printf(" -> NO I2C DEVICES FOUND! Check wiring/pull-ups.\n");
    }
    printf("--- Scan Complete ---\n\n");
    fflush(stdout);
}

uint8_t color;
    uint8_t img = 0;
    DFRobot_RGBPanel_img_t test_img1 = (DFRobot_RGBPanel_img_t){
        .x = 1,
        .y = 1,
        .width = 3,
        .height = 3,
        .data = (uint8_t[]){
            RED, RED, RED, 
            RED, QUENCH, RED,
            RED, RED, RED
        }
    };
    
    DFRobot_RGBPanel_img_t test_img2 = (DFRobot_RGBPanel_img_t){
        .x = 12,
        .y = 1,
        .width = 3,
        .height = 3,
        .data = (uint8_t[]){
            CYAN, QUENCH, CYAN, 
            QUENCH, CYAN, QUENCH,
            CYAN, QUENCH, CYAN
        }
    };

    DFRobot_RGBPanel_img_t test_img3 = (DFRobot_RGBPanel_img_t){
        .x = 1,
        .y = 6,
        .width = 14,
        .height = 2,
        .data = (uint8_t[]){
            WHITE, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, WHITE,
            QUENCH, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, QUENCH,
        }
    };


int main() {
    stdio_init_all();
    sleep_ms(5000); // Wait for USB to be connected
    printf("\n--- Pico W Started ---\n");
    fflush(stdout);
    
    init_spi();
    init_i2c();

    sleep_ms(5000); // Wait for peripherals to be ready
    scan_i2c_bus(); // Scan the I2C bus for connected devices
    // Give the panel MCU a brief settling time post-I2C init
    sleep_ms(100);

    RGBPanel_init(&rgb_panel, I2C_PORT, _RGBAddr);
    sleep_ms(100); // Allow time for the panel to initialize

    // Set control mode flags (Disable scrolling, enable standard color operations)
    // rgb_panel.buf[0] = (0x01 << 3); // Flag bit set for static color/pixel writes

    // Clear and fill screen
    RGBPanel_clear(&rgb_panel);
    // RGBPanel_fillScreen(&rgb_panel, QUENCH); // Fill screen with RED
    sleep_ms(500);

    // RGBPanel_pixel(&rgb_panel, 0, 0, 0x03); // Set pixel at (0,0) to RED
    // RGBPanel_pixel(&rgb_panel, 15, 7, 0x02); // Set pixel at (15,7) to GREEN
    // Fill screen with RED (0x01)
    // RGBPanel_fillAll(&rgb_panel, RED);
    uint8_t color = 0x00; // RED0

    RGBPanel_img_draw(&rgb_panel, &test_img1);
    RGBPanel_img_draw(&rgb_panel, &test_img2);
    RGBPanel_img_draw(&rgb_panel, &test_img3);
    while (true) {
        printf("Hello, world! Color: 0x%02X\n", color);
        // for (uint8_t y = 0; y < 8; y++) {
            // for (uint8_t x = 0; x < 16; x++) {
            //     RGBPanel_pixel(&rgb_panel, x, color, 0x04);
            // }
        // }

        color = (color + 1) % 8; // Cycle through colors 0-7
        
        sleep_ms(1000);

        // if (color == 0) {
        //     RGBPanel_clear(&rgb_panel); // Clear the panel when cycling back to 0
        //     sleep_ms(500);
        // }
    }
}
