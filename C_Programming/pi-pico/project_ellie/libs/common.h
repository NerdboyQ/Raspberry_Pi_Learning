#ifndef UNIVERSAL_COMMON_H
#define UNIVERSAL_COMMON_H

#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "pico/flash.h"
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/flash.h"
#include "hardware/i2c.h"
#include "hardware/spi.h"
#include "hardware/sync.h"

/**
 * @brief Flash read/write base address, this will
 * be used for long-term storage in flash memory.
 * 
 * The Pi Pico W has 2MB of memory from 0x10000000-0x10200000;
 * this value limits the read/write area to ~512kB
 * 
 * e.g. gif frames, wifi credentials, etc
 */
#define FLASH_RW_BASE _u(0x10180000)

/**
 * @brief Calculate the offset of a flash address relative to the read/write base.
 *
 * flash write functions are based on offsets not absolute addresses.
 *  
 * @param addr The absolute flash address.
 * @return The offset from XIP_BASE.
 */
#define FLASH_OFFSET(addr) _u((addr) - XIP_BASE)

/**
 * @brief Base address for storing WiFi credentials in flash memory.
 */
#define FLASH_WIFI_CREDENTIALS_BASE _u(0x101B2140)

#pragma pack(push, 1)

/**
 * @brief Structure representing WiFi credentials (SSID and password).
 */
typedef struct {
    uint8_t ssid[32]; // wifi name up to 31 characters not including null terminator
    uint8_t password[32];
} wifi_credentials_t;

#pragma pack(pop)

#endif // UNIVERSAL_COMMON_H
