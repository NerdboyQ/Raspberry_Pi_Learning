/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "main.h"

bool test_write_flash_data(uint8_t idx) {
    // Check if the flash already contains the data
    if (!memcmp(ld_buf, (uint32_t*)FLASH_RW_BASE + (idx*FLASH_GIF_FRAME_SPAN), FLASH_GIF_FRAME_SPAN)) return true;
    
    // Disable interrupts to ensure atomic flash write operations
    uint32_t intr = save_and_disable_interrupts();

    // Erase flash area before writing new data
    for (int i = 0; i < FLASH_GIF_PAGE_CNT; i++) {
        flash_range_erase(
            FLASH_GIF_ADDRESS(0) - XIP_BASE + (idx*FLASH_GIF_FRAME_SPAN) + (FLASH_SECTOR_SIZE * i), 
            FLASH_SECTOR_SIZE);
    }

    // this write the 1st jabber bitmap to flash
    flash_range_program(
        FLASH_GIF_ADDRESS(0) - XIP_BASE + (idx*FLASH_GIF_FRAME_SPAN), 
        ld_buf, 
        FLASH_GIF_FRAME_SPAN);

    // Restore interrupts after flash write operations
    restore_interrupts(intr);

    return false;
}

void load_anime_neko_bitmaps() {
    for (uint8_t n=0; n < GIF_MAX_FRAME_CNT; n++){
        switch (n) {
            case 0:
                memcpy(ld_buf, jabber_frame_000, (FLASH_GIF_FRAME_SPAN));
                break;
            case 1:
                memcpy(ld_buf, jabber_frame_001, (FLASH_GIF_FRAME_SPAN));
                break;
            case 2:
                memcpy(ld_buf, jabber_frame_002, (FLASH_GIF_FRAME_SPAN));
                break;
            case 3:
                memcpy(ld_buf, jabber_frame_003, (FLASH_GIF_FRAME_SPAN));
                break;
            case 4:
                memcpy(ld_buf, jabber_frame_004, (FLASH_GIF_FRAME_SPAN));
                break;
            case 5:
                memcpy(ld_buf, jabber_frame_005, (FLASH_GIF_FRAME_SPAN));
                break;
            case 6:
                memcpy(ld_buf, jabber_frame_006, (FLASH_GIF_FRAME_SPAN));
                break;
            case 7:
                memcpy(ld_buf, jabber_frame_007, (FLASH_GIF_FRAME_SPAN));
                break;
            case 8:
                memcpy(ld_buf, jabber_frame_008, (FLASH_GIF_FRAME_SPAN));
                break;
            case 9:
                memcpy(ld_buf, jabber_frame_009, (FLASH_GIF_FRAME_SPAN));
                break;
            default:
                break;
        }
        test_write_flash_data(n);
    }
}

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
    display_init(spi0, SPI_PIN_RST, SPI_PIN_DC, -1, &gs_handle);
    sleep_ms(100); // Allow time for the panel to initialize
    st7789_clear(&gs_handle); // Clear the display to black
    sleep_ms(100); // Allow time for the clear command to take effect
    
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
    uint8_t img = 0;
    DFRobot_RGBPanel_img_t test_img1 = (DFRobot_RGBPanel_img_t){
        .x = 1,
        .y = 1,
        .width = 3,
        .height = 3,
        .data = (uint8_t[]){
            GREEN, GREEN, GREEN, 
            GREEN, QUENCH, GREEN,
            GREEN, GREEN, GREEN
        }
    };
    
    DFRobot_RGBPanel_img_t test_img2 = (DFRobot_RGBPanel_img_t){
        .x = 12,
        .y = 1,
        .width = 3,
        .height = 3,
        .data = (uint8_t[]){
            PURPLE, QUENCH, PURPLE, 
            QUENCH, PURPLE, QUENCH,
            PURPLE, QUENCH, PURPLE
        }
    };

    DFRobot_RGBPanel_img_t test_img3 = (DFRobot_RGBPanel_img_t){
        .x = 1,
        .y = 6,
        .width = 14,
        .height = 2,
        .data = (uint8_t[]){
            CYAN, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, QUENCH, CYAN,
            QUENCH, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, QUENCH,
        }
    };
    
    RGBPanel_img_draw(&rgb_panel, &test_img1);
    RGBPanel_img_draw(&rgb_panel, &test_img2);
    RGBPanel_img_draw(&rgb_panel, &test_img3);
    
    // test_display_color_channels(&gs_handle); // Display RED color on the ST7789 panel
    load_anime_neko_bitmaps();
    uint8_t frame_idx = 0;
    while (true) {
        // GOTCHA : The bitmap/frames are written as 16bit RGB565 values, but when written
        // to flash the size reference is in bytes (not words). So when reading 
        // as 16bit values we need to divide the byte offset by 2.
        // NOTE: The function reads pixel values not bytes, hence the division by 2.
        st7789_draw_picture_16bits(&gs_handle, 0, 0, 127, 127, (uint16_t *)FLASH_GIF_ADDRESS(0) + (frame_idx * (FLASH_GIF_FRAME_SPAN >> 1)));
        frame_idx = (frame_idx + 1) % GIF_MAX_FRAME_CNT;
        sleep_ms(100); // Add a small delay to control the frame rate
        // printf("Hello, world! Color: 0x%02X\n", color);
        // for (uint8_t y = 0; y < 8; y++) {
            // for (uint8_t x = 0; x < 16; x++) {
            //     RGBPanel_pixel(&rgb_panel, x, color, 0x04);
            // }
        // }

        // color = (color + 1) % 8; // Cycle through colors 0-7
        
        // sleep_ms(1000);

        // if (color == 0) {
        //     RGBPanel_clear(&rgb_panel); // Clear the panel when cycling back to 0
        //     sleep_ms(500);
        // }
    }
}
