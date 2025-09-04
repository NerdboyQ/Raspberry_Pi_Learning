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

int getIdx(char c) { return c == '.' ? 0 : c - '0'; }

bool isValidSudoku (char *board) {
    if (strlen(board) != 81) return false;

    for (int r = 0; r < 9; r+=3) {
        int row[10] = {0};
        int cols[9][10] = {0};
        for (int c = 0; c < 9; c+=3) {
            int blk[10] = {0};
            // char rch = *(board + (r*9) + (c));
            for (int hr = 0; hr < 3; hr+=1) {
                int tr = r*9+hr*9;
                // char rch = *(board + tr + (c));
                // printf(" %c", rch);
                for (int hc = 0; hc < 3; hc+=1) {
                    char ch1 = *(board + tr + (c+hc));
                    if (ch1 != '.') {
                        blk[getIdx(ch1)]+=1;
                        // printf("%c, idx: %d, val: %d\n", ch1, getIdx(ch1), blk[getIdx(ch1)]);
                        if (blk[getIdx(ch1)]-1) return false;
                    }
                    // printf(" %c", ch1);
                    if (!isValidChar(ch1)) return false;
                }
                // printf(" | \n");
            }
            printf("------\n");
        }
    }

    return true;
}
// bool isValidSudoku (char *board) {
//     if (strlen(board) != 81) return false;
//     int cols[9][9] = {0};
    
//     char ch;
//     for (int r = 0; r < 9; r+=3) {
//         int row[9] = {0};
//         for (int c = 0; c<9; c++) {
//             int hws[9] = {0};
//             ch = *(board +(r*9) + c);
//             // printf("char: %c, i: %d\n", ch, (int)(ch-'1'));
            
//             if (!isValidChar(ch)) return false;

//             char ch2 = *(board +((r+1)*9) + c);
//             char ch3 = *(board +((r+2)*9) + c);
//             if (!isValidChar(ch2) | !isValidChar(ch3)) return false;

//             // check house
//             if (!c| ((c+1) % 3 ==0 & c < 8) ){
//                 for (int h = 0; h< 3;h++) {
                    
//                 }
//             }
            
            
//             if (ch != '.') {
//                 // check row
//                 row[(int)(ch-'1')]+=1;
//                 if (row[(int)(ch-'1')]-1 > 0) return false;
                
//                 // check col
//                 cols[c][ch-'1']+=1;
                
//                 if (ch2 != '.') cols[c][ch2-'1']+=1;
//                 if (ch3 != '.') cols[c][ch3-'1']+=1;
//                 if (cols[c][(int)(ch-'1')]-1 > 0 |
//                     cols[c][(int)(ch2-'1')]-1 > 0 |
//                     cols[c][(int)(ch3-'1')]-1 > 0) return false;

                
//             }
            
//         }
//     }

//     return true;
// }



int main(int argc, char **kwargs) {
    Test_t tests[5] = {
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
        }
    };
    

    // Test_t tests[4] = {
    //     test_valid,
    //     test_invalid_col,
    //     test_invalid_row,
    //     test_invalid_hws
    // };
    
    for (int i=0; i<5; i++) {
        Test_t test = tests[i];
        // print_board(test.board); break;
        printf("[%s] %s\n", test.title, isValidSudoku(test.board) ? "true" : "false");
    }
    
    // printf("%s\n", isValidSudoku(test_invalid_col.board) ? "true" : "false");
    // printf("%s\n", isValidSudoku(test_invalid_row.board) ? "true" : "false");
    // printf("%s\n", isValidSudoku(test_invalid_hws.board) ? "true" : "false");
    return 0;
}
