#ifndef MAIN_H
#define MAIN_H

#include "DFRobot_RGBPanel/DFRobot_RGBPanel.h"
#include "Display/_gif_test.h"

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
static st7789_handle_t gs_handle;        /** st7789 handle */

// Buffer for storing data read from flash memory sectors
static uint8_t ld_buf[FLASH_GIF_FRAME_SPAN];

#endif // MAIN_H
