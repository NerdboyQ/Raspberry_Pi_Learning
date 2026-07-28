#include "DFRobot_RGBPanel.h"


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
