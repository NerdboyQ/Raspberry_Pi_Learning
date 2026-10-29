#include "graphics.h"

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

/**
 * Test Color channels & Dimensions
 * 
 * @param handle: st7789 display handle
 */
 void test_display_color_channels (st7789_handle_t *handle) {
    /**
     * The DFD Robot 240x320 display uses the st7789. It is a 16bit color display 
     * w/ the RGB 565 color encoding:
     * 
     *      0000|0 000|000 0|0000
     * Full Red  :  0xF800 (upper  5 bits)
     * Full Green:  0x07E0 (center 6 bits)
     * Full Blue :  0x001F (lower  5 bits)
     */
    printf("Test 1: Red rectangle\n");
    st7789_fill_rect(handle, 10, 10, 110, 110, 0xf800);
    sleep_ms(2000);
    
    // Test 2: Green rectangle
    printf("Test 2: Green rectangle\n");
    st7789_fill_rect(handle, 130, 10, 230, 110, 0x07E0);
    sleep_ms(2000);
    
    // Test 3: Blue rectangle
    printf("Test 3: Blue rectangle\n");
    st7789_fill_rect(handle, 10, 140, 110, 240, 0x001F);
    sleep_ms(2000);

    // Test 4: Gray rectangle
    printf("Test 4: Grey rectangle\n");
    st7789_fill_rect(handle, 130, 140, 230, 240, 0x8410);
    sleep_ms(2000);

    printf("Test: All bits on (0xFFFF - should be white)\n");
    st7789_fill_rect(handle, 0, 240, 239, 319, 0xFFFF);
    sleep_ms(3000);

    // Test combinations
    printf("Test: Red + Green (0xF7E0 - should be yellow)\n");
    st7789_fill_rect(handle, 0, 0, 119, 159, 0xFFE0);
    sleep_ms(3000);

    printf("Test: Red + Blue (0xF81F - should be magenta)\n");
    st7789_fill_rect(handle, 120, 0, 239, 159, 0xF81F);
    sleep_ms(3000);

    printf("Test: Green + Blue (0x07FF - should be cyan)\n");
    st7789_fill_rect(handle, 0, 160, 119, 319, 0x07FF);
 }

/**
 * Simple function to test basic st7789 initialization of color display
 * 
 * @return false if no issue occurs with the test, otherwise return true
 */
bool test_spi_display() {
    // Initialize st7789 handle & display data structure
    static st7789_handle_t g_st7789_handle;
    static bool initialized = false;

    static sprite_t nerdboyq_sprite, demo_sprite;

    // Only initialize once
    if (!initialized) {
        printf("Intializing display\n");
        // display_err_t init_status = display_init(true, SPI_PIN_RST, SPI_PIN_DC, -1, &g_st7789_handle);
        // if (init_status) {
        //     printf(" !ERROR: failure %d: ", init_status);
        //     switch (init_status) {
        //         case displaySts_fail_alloc:
        //             printf("FAILED MEMORY ALLOCATION\n");
        //             break;
        //         case displaySts_fail_comm:
        //             printf("FAILED COMMUNICATION\n");
        //             break;
        //         case displaySts_fail_init:
        //             printf("FAILED INIT\n");
        //             break;
        //         case displaySts_fail_param:
        //             printf("BAD PARAMS\n");
        //             break;
                    
        //         default:
        //             printf("UNKNOWN ERROR\n");
        //             break;
        //     }
        //     return true;
        // }

        initialized = true;
        // Clear screen
        printf("Clearing screen...\n");
        st7789_clear(&g_st7789_handle);
        sleep_ms(1000);
        
        sprite_create(&demo_sprite,
            demo_green_hair_sprite,
            32*32,
            32,
            32
        );

        sprite_create(&nerdboyq_sprite,
            nerdboyq_alien_demo,
            32*32,
            32,
            32
        );
    }

    printf("Starting tests...\n\n");

    static uint16_t left, top;
    static bool left_move = false;
    if (nerdboyq_sprite.position.left == nerdboyq_sprite.position.right) {
        left = 10;
        top = 10;
        // the offsets need to be the height & width of the image, inclusive to the starting pixel column/row
        sprite_draw_at_pos(&g_st7789_handle, &demo_sprite, left, top);
        sleep_ms(3000);
        sprite_draw_at_pos(&g_st7789_handle, &nerdboyq_sprite, left+31+10, top);
        sleep_ms(3000);
    } else {
        if (!left_move) {
            top+=2;
        } else {
            top-=2;
        }
        sprite_move_to_pos(&g_st7789_handle, &demo_sprite, left, top);
        sprite_move_to_pos(&g_st7789_handle, &nerdboyq_sprite, left+31+10, top);

        if (top >= 320-32) left_move = true;
        else if (top <= 10) left_move = false;
        sleep_us(5);
    }

    printf("All tests complete!\n");

    return false;
}
