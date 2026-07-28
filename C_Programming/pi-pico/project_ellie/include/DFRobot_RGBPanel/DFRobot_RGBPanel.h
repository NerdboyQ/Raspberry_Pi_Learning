#ifndef __DFRobot_RGB_H__
#define __DFRobot_RGB_H__

#include "libs/common.h"

#define REG_COMMAND     0x00  // Command Register Index
#define REG_DISPLAY_RAM 0x02  // RAM Matrix Register Index

// HT1632C Command Byte Masks
#define HT1632_SYS_DIS  0x00  // Turn off oscillator
#define HT1632_SYS_EN   0x01  // Enable system oscillator
#define HT1632_LED_OFF  0x02  // Turn off LED duty generator
#define HT1632_LED_ON   0x03  // Turn on LEDs
#define HT1632_PWM_MAX  0xAF  // Set maximum PWM brightness (16/16)

#define _RGBAddr 0x10
#define FUNC 0x02
#define COLOR 0x03
#define PIX_X 0x04
#define PIX_Y 0x05
#define BITMAP 0x06
#define STR 0x07

#define UNCLEAR 0x0
#define CLEAR 0x1
#define Left (0x0 << 1)
#define Right (0x1 << 1)
#define None (0x11)
#define UNSCROLL (0x0 << 2)
#define SCROLL (0x1 <<2)
#define PIX_ENABLE (0x01 << 3)
#define BITMAP_ENABLE (0x10 << 3)
#define STR_ENABLE (0x11 << 3)

#define QUENCH 0
#define RED 1
#define GREEN 2
#define YELLOW 3
#define BLUE 4
#define PURPLE 5
#define CYAN 6
#define WHITE 7

#define SIZE 50
// This delay was used for 1MHz I2C speed
#define RGB_W_MIN_DELAY 5

/**
 * @brief Structure representing the DFRobot RGB Panel.
 * 
 * This structure contains a buffer to hold the data for the RGB panel.
 * The buffer size is defined by the SIZE constant.
 */
typedef struct {
    i2c_inst_t *i2c_port;
    uint8_t i2c_addr;
    unsigned char buf[SIZE];
} DFRobot_RGBPanel_t;

/**
 * @brief Initializes the DFRobot RGB Panel.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param i2c_port Pointer to the I2C instance to use for communication.
 * @param i2c_addr I2C address of the RGB panel.
 * 
 */
void RGBPanel_init(DFRobot_RGBPanel_t *panel, i2c_inst_t *i2c_port, uint8_t i2c_addr);

/**
 * @brief Scroll the display in a specified direction.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param dir Direction to scroll (None, Right, Left).
 * 
 */
void RGBPanel_scroll(DFRobot_RGBPanel_t *panel, unsigned char dir);

/**
 * @brief Display a picture on the RGB panel.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param picIndex Index of the picture to display (0-7).
 * @param color Color to use for the picture (0-7).
 * 
 */
void RGBPanel_display(DFRobot_RGBPanel_t *panel, unsigned char picIndex,unsigned char color);

/**
 * @brief Print characters on the RGB panel.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param s String to print.
 * @param color Color to use for the text (0-7).
 * 
 */
void RGBPanel_print_chars(DFRobot_RGBPanel_t *panel, char *s,unsigned char color);

/**
 * @brief Set a pixel on the RGB panel.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param x X-coordinate of the pixel (0-7).
 * @param y Y-coordinate of the pixel (0-7).
 * @param color Color to use for the pixel (0-7).
 * 
 */
void RGBPanel_pixel(DFRobot_RGBPanel_t *panel, unsigned char x,unsigned char y,unsigned char color);

/**
 * @brief Fill the entire RGB panel with a specified color.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param color Color to fill the screen with (0-7).
 * 
 */
void RGBPanel_fillScreen(DFRobot_RGBPanel_t *panel, unsigned char color);

/**
 * @brief Fill all pixels on the RGB panel with a specified color.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param color Color to fill all pixels with (0-7).
 */
void RGBPanel_fillAll(DFRobot_RGBPanel_t *panel, unsigned char color);

/**
 * @brief Clear the RGB panel.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * 
 */
void RGBPanel_clear(DFRobot_RGBPanel_t *panel);

/**
 * @brief Read a register from the RGB panel.
 * 
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param addr Address of the register to read.
 * @param num Number of bytes to read.
 * 
 * @return Pointer to an array containing the read data.
 * 
 */
int* RGBPanel_readReg(DFRobot_RGBPanel_t *panel, uint8_t addr, uint8_t num);

/**
 * @brief Set a register on the RGB panel.
 * @param panel Pointer to the DFRobot_RGBPanel_t structure.
 * @param Reg Register to set.
 * @param pdata Pointer to the data to write to the register.
 * @param datalen Length of the data to write (max 7).
 * 
 */
void RGBPanel_setReg(DFRobot_RGBPanel_t *panel, unsigned char Reg ,unsigned char *pdata, unsigned char datalen );

#endif
