#include "display_spi.h"
#include "driver_st7789.h"
#include "graphics.h"
#include <stdint.h>

/**
 * Create sprite
 * 
 */
bool sprite_create(sprite_t *sprite, uint16_t *img, uint16_t N, uint16_t width, uint16_t height) {
    sprite->dimensions = (sprite_dimensions_t) {
        .width = width,
        .height = height
    };

    sprite->array_length = N;
    sprite->img = img;
}

/**
 * Draw sprite
 * 
 * @param handle: st7789 display handle
 */
void sprite_draw_at_pos (st7789_handle_t* handle, sprite_t *sprite, uint16_t left, uint16_t top) {
    // update current to new position
    sprite->position.left = left;
    sprite->position.top = top;
    sprite->position.right = left + sprite->dimensions.width - 1; // account for inclusive 1st pixel in row
    sprite->position.bottom = top + sprite->dimensions.height - 1; // account for inclusive 1st pixel in column

    // draw in new positions
    st7789_draw_picture_16bits(handle,
        sprite->position.left,
        sprite->position.top,
        sprite->position.right,
        sprite->position.bottom,
        sprite->img
    );
}

/**
 * Clear sprite from display
 * 
 * @param handle: st7789 display handle
 */
void sprite_remove_image(st7789_handle_t* handle, sprite_t *sprite) {
    st7789_fill_rect(handle, 
        sprite->position.left, 
        sprite->position.top, 
        sprite->position.right, 
        sprite->position.bottom, 
        0x0000);
}

/**
 * Update sprite position
 * 
 * @param handle: st7789 display handle
 */
void sprite_move_to_pos (st7789_handle_t* handle, sprite_t *sprite, uint16_t left, uint16_t top) {
    
    sprite_position_t old_pos = (sprite_position_t){
        .left = sprite->position.left,
        .right = sprite->position.right,
        .top = sprite->position.top,
        .bottom = sprite->position.bottom
    };
    // redraw at new position
    sprite_draw_at_pos(handle, sprite, left, top);

    // erase old +/- x direction
    if (sprite->position.left < old_pos.left) {
        st7789_fill_rect(handle, 
        sprite->position.right+1, 
        sprite->position.top, 
        old_pos.right, 
        sprite->position.bottom, 
        0x0000);
    } else if (sprite->position.left > old_pos.left) {
        st7789_fill_rect(handle, 
        old_pos.left, 
        sprite->position.top, 
        sprite->position.left-1, 
        sprite->position.bottom, 
        0x0000);
    }

    // erase old +/- y direction
    if (sprite->position.top < old_pos.top) {
        st7789_fill_rect(handle, 
        sprite->position.left,
        sprite->position.bottom+1,
        sprite->position.right, 
        old_pos.bottom, 
        0x0000);
    } else if (sprite->position.top > old_pos.top) {
        st7789_fill_rect(handle, 
        sprite->position.left,
        old_pos.top,
        sprite->position.right,
        sprite->position.top+1, 
        0x0000);
    }
    
    
}