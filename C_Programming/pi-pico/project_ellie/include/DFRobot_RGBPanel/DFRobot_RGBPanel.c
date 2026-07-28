#include "DFRobot_RGBPanel.h"

DFRobot_RGBPanel_img_t* RGBPanel_img_init(uint8_t x, uint8_t y, uint8_t width, uint8_t height, uint8_t *data) {
    // Verify valid dimensions and position
    if (!(width*height) || width > RGBPANEL_MAX_W || height > RGBPANEL_MAX_H) {
        printf("Invalid image dimensions: width=%d, height=%d\n", width, height);
        return NULL;
    }
    if (!(x*y) || x >= RGBPANEL_MAX_W || y >= RGBPANEL_MAX_H || (x + width) > RGBPANEL_MAX_W || (y + height) > RGBPANEL_MAX_H) {
        printf("Invalid image position: x=%d, y=%d\n", x, y);
        return NULL;
    }

    // Verify that the data pointer is not NULL and that the color values are valid
    if (!data) {
        printf("Data pointer is NULL for image at (%d, %d) with dimensions (%d, %d)\n", x, y, width, height);
        return NULL;
    }
    for (int i=0; i < height*width; i++) {
        if (!IS_VALID_COLOR(data[i])) {
            printf("Invalid color value %d at index %d for image at (%d, %d) with dimensions (%d, %d)\n", data[i], i, x, y, width, height);
            return NULL;
        }
    }

    DFRobot_RGBPanel_img_t *img = (DFRobot_RGBPanel_img_t *)malloc(sizeof(DFRobot_RGBPanel_img_t));
    if (!img) {
        printf("Memory allocation failed for image at (%d, %d) with dimensions (%d, %d)\n", x, y, width, height);
        return NULL;
    }
    
    img->x = x;
    img->y = y;
    img->width = width;
    img->height = height;
    img->data = data;
    return img;
}

void RGBPanel_img_destroy(DFRobot_RGBPanel_img_t *img) {
    if (!img) return;
    img->data = NULL;
    free(img);
}

void RGBPanel_img_draw(DFRobot_RGBPanel_t *panel, DFRobot_RGBPanel_img_t *img) {
    if (!panel || !img) return;

    for (uint8_t row = 0; row < img->height; row++) {
        for (uint8_t col = 0; col < img->width; col++) {
            uint8_t color = img->data[row * img->width + col];
            RGBPanel_pixel(panel, img->x + col, img->y + row, color);
        }
    }
}

void RGBPanel_init(DFRobot_RGBPanel_t *panel, i2c_inst_t *i2c, uint8_t addr) {
    if (!panel) return;
    panel->i2c_port = i2c;
    panel->i2c_addr = addr;

    // 1. Wake up internal oscillator (SYS EN)
    uint8_t sys_en_cmd = HT1632_SYS_EN;
    RGBPanel_setReg(panel, REG_COMMAND, &sys_en_cmd, 1);
    sleep_ms(10);

    // 2. Turn on display output (LED ON)
    uint8_t led_on_cmd = HT1632_LED_ON;
    RGBPanel_setReg(panel, REG_COMMAND, &led_on_cmd, 1);
    sleep_ms(10);

    // 3. Set brightness to maximum (16/16 PWM)
    uint8_t pwm_cmd = HT1632_PWM_MAX;
    RGBPanel_setReg(panel, REG_COMMAND, &pwm_cmd, 1);
    sleep_ms(10);

    // Clear RAM buffer
    memset(panel->buf, 0, sizeof(panel->buf));
}

void RGBPanel_setReg(DFRobot_RGBPanel_t *panel, unsigned char Reg, unsigned char *pdata, unsigned char datalen) {
    if (!panel || !panel->i2c_port) return;
    uint8_t tx_buf[SIZE + 1];
    tx_buf[0] = Reg;
    memcpy(&tx_buf[1], pdata, datalen);
    int ret = i2c_write_blocking(panel->i2c_port, panel->i2c_addr, tx_buf, datalen + 1, false);
    if (ret < 0) {
        printf("I2C write failed for reg 0x%02X (ret=%d)\n", Reg, ret);
    }
}

void RGBPanel_clear(DFRobot_RGBPanel_t *panel) {
    if (!panel) return;
    panel->buf[0] = CLEAR;
    for (int i = 1; i < SIZE; i++) panel->buf[i] = 0;
    RGBPanel_setReg(panel, FUNC, panel->buf, SIZE);   // always SIZE bytes, not 35
    sleep_ms(SIZE * RGB_W_MIN_DELAY); // Delay to ensure the command is processed
}

void RGBPanel_fillScreen(DFRobot_RGBPanel_t *panel, unsigned char color) {
    if (!panel) return;
    panel->buf[0] = CLEAR;
    panel->buf[0] = (panel->buf[0] & 0xe7) | PIX_ENABLE;
    panel->buf[1] = color;
    panel->buf[2] = 0;
    panel->buf[3] = 0;
    RGBPanel_setReg(panel, FUNC, panel->buf, SIZE);
    sleep_ms(SIZE * RGB_W_MIN_DELAY); // Delay to ensure the command is processed
}

void RGBPanel_fillAll(DFRobot_RGBPanel_t *panel, unsigned char color) {
    for (uint8_t y = 0; y < 8; y++) {
        for (uint8_t x = 0; x < 16; x++) {
            RGBPanel_pixel(panel, x, y, color);
        }
    }
}

void RGBPanel_pixel(DFRobot_RGBPanel_t *panel, unsigned char x, unsigned char y, unsigned char color) {
    if (!panel) return;
    panel->buf[0] = (panel->buf[0] & 0xe6) | PIX_ENABLE;
    panel->buf[1] = color;
    panel->buf[2] = x;
    panel->buf[3] = y;
    RGBPanel_setReg(panel, FUNC, panel->buf, SIZE);   // full buffer every call
    sleep_ms(RGB_W_MIN_DELAY); // small delay to ensure the command is processed
}

void RGBPanel_display(DFRobot_RGBPanel_t *panel, unsigned char picIndex, unsigned char color) {
    panel->buf[0] = (panel->buf[0] & 0xe6) | (0x02 << 3); // Set the PIX_ENABLE bit
    panel->buf[1] = color; // Set the color for the display
    panel->buf[4] = picIndex; // Set the picture index to display
    RGBPanel_setReg(panel, FUNC, panel->buf, SIZE); // Send the command to the panel
    sleep_ms(SIZE * RGB_W_MIN_DELAY); // Delay to ensure the command is processed
}
