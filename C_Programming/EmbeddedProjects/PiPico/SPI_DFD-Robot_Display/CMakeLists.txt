# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico_w CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(spi_st7789_display C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()


# adding driver for display
add_library(driver_st7789
    lib/driver_st7789/driver_st7789.c
    lib/driver_st7789/driver_st7789.h
    lib/driver_st7789/driver_st7789_font.h
    )

# Add executable. Default name is the project name, version 0.1
add_executable(spi_st7789_display main.c)

# adding directories to target
target_include_directories(driver_st7789 PUBLIC lib/driver_st7789)

# pull in common dependencies
target_link_libraries(spi_st7789_display 
    pico_stdlib
    hardware_spi
    hardware_dma
    driver_st7789
    )

# Enable USB serial output for printf
pico_enable_stdio_usb(spi_st7789_display 1)
pico_enable_stdio_uart(spi_st7789_display 0)

# linking driver directory
target_link_directories(spi_st7789_display PRIVATE driver_st7789 )

if (PICO_CYW43_SUPPORTED)
    target_link_libraries(spi_st7789_display pico_cyw43_arch_none)
endif()

# create map/bin/hex file etc.
pico_add_extra_outputs(spi_st7789_display)

# add url via pico_set_program_url