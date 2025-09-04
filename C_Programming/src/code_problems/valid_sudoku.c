#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

typedef struct {
    char title[20];
    char *board;
    bool answer;
} Test_t;

void print_board(char *board) {

    for (int r=0; r < 9; r+=1) {
        for (int c = 0; c<9;c++) {
            if (!c) printf("%c", *(board +(r*9) + c));
            else printf(" %c", *(board +(r*9) + c));
            if (c > 0 & (c+1)%3 == 0 & c < 8) printf("|");
        }

        printf("\n");
        if (r > 0 & (r+1) % 3 == 0 & r < 8) printf("-------------------\n");
    }
}

bool isValidChar(char c) { return c == '.' | (c >= '1' & c <= '9'); }

int getIdx(char c) { return c == '.' ? 0 : c - '1'; }

bool isValidSudoku (char *board) {
    if (strlen(board) != 81) return false;

    int blks[9][9] = {};
    int rows[9][9] = {};
    int cols[9][9] = {};

    for (int i =0; i < 81; i++) {
        int row_i = i/9;
        int col_i = i%9;
        int blk_i = row_i/3*3+col_i/3;
        char chr = *(board+i);
        int idx = getIdx(chr);
        if (!isValidChar(chr)) return false;
        if (chr !='.') {
            if (rows[row_i][idx]) return false;
            if (cols[col_i][idx]) return false;
            if (blks[blk_i][idx]) return false;
            rows[row_i][idx]+=1;
            cols[col_i][idx]+=1;
            blks[blk_i][idx]+=1;
        }
        // printf("{[blk-%d] row: %d, col: %d, char: %c}\n", blk_i, row_i, col_i, chr);
    }

    return true;
}

int main(int argc, char **kwargs) {
    Test_t tests[8] = {
        (Test_t){
            .title = "valid",
        .board = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79",
        /**
           5 3 .| . 7 .| . . .
           6 . .| 1 9 5| . . .
           . 9 8| . . .| . 6 .
           -------------------
           8 . .| . 6 .| . . 3
           4 . .| 8 . 3| . . 1
           7 . .| . 2 .| . . 6
           -------------------
           . 6 .| . . .| 2 8 .
           . . .| 4 1 9| . . 5
           . . .| . 8 .| . 7 9
         */
        .answer=true
        },
        (Test_t){
            .title = "invalid_rows",
            .board = "53.57....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79",
            .answer=false
        },
        (Test_t){
            .title = "invalid_cols",
            .board = "53..7....6..195....98....6.5...6...34..8.3..17...2...6.6....28....419..5....8..79",
            .answer=false
        },
        (Test_t){
            .title = "invalid_blks",
            .board = "53..7....65.195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79",
            .answer=false
        },
        (Test_t){
            .title = "invalid_char",
            .board = "53..7....65.195....z8....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79",
            .answer=false
        },
        (Test_t){
            .title = "invalid_length",
            .board = "53..7....65.195....z8....6.8...6...34..8.3..17...2...6.6....28....419..5",
            .answer=false
        },
        (Test_t){
            .title = "invalid_corner_case1",
            .board = "53.57....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79",
            .answer=false
        },
        (Test_t){
            .title = "invalid_corner_case2",
            .board = "53..7....6..195....98....6.888.6...34..8.3..17...2...6.6....28....419..5....8..79",
            .answer=false
        },
    };
    
    for (int i=0; i<8; i++) {
        Test_t test = tests[i];
        printf("Test_%s:\n", test.title);
        bool answer = isValidSudoku(test.board);
        printf(" %s - %s\n", answer ? "true" : "false", answer == test.answer ? "correct answer" : "incorrect answer");
        // break;
    }
    
    return 0;
}
