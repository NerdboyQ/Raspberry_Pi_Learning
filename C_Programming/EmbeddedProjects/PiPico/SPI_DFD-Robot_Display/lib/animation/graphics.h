#ifndef GRAPHICS_H
#define GRAPHICS_H

#include "driver_st7789.h"
#include <stdint.h>

typedef struct {
    uint16_t height, width;
} sprite_dimensions_t;

typedef struct {
    uint16_t left, top, right, bottom;
} sprite_position_t;

typedef struct {
    uint16_t *img;
    uint16_t array_length;
    sprite_dimensions_t dimensions;
    sprite_position_t position;
} sprite_t;

// Motion directions
typedef enum {
    N_, // UP
    NE, // UP-RIGHT
    E_, // RIGHT
    SE, // DOWN-RIGHT
    S_, // DOWN
    SW, // DOWN-LEFT
    W_, // LEFT
    NW, // UP-LEFT
} sprite_motion_dir_t;

/**
 * Create sprite
 * 
 */
bool sprite_create(sprite_t *sprite, uint16_t *img, uint16_t N, uint16_t width, uint16_t height);

/**
 * Draw sprite
 * 
 * @param handle: st7789 display handle
 */
void sprite_draw_at_pos (st7789_handle_t* handle, sprite_t *sprite, uint16_t left, uint16_t top);

/**
 * Clear sprite from display
 * 
 * @param handle: st7789 display handle
 */
void sprite_remove_image(st7789_handle_t* handle, sprite_t *sprite);

/**
 * Update sprite position
 * 
 * @param handle: st7789 display handle
 */
void sprite_move_to_pos (st7789_handle_t* handle, sprite_t *sprite, uint16_t left, uint16_t top);

#endif