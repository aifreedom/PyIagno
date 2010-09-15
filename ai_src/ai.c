#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <assert.h>
#include "ai.h"

#define BRD_WIDTH 8
#define BRD_HEIGHT 8

#define in_board(x, y) ((x)>=0 && (x)<BRD_HEIGHT && (y)>=0 && (y)<BRD_WIDTH)

enum {BRD_BLANK=-1, BRD_DARK, BRD_LIGHT};

static void get_valid(int board[8][8], int player, int *valid, int *valid_cnt);
static int is_valid(int board[8][8], int player, int pos);

// static void get_valid(int board[8][8], int player, int *valid, int *valid_cnt);
// static int is_valid(int board[8][8], int player, int pos);

const int dir[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1},
                       {1, -1}, {1, 0}, {1, 1}};

                        
int easy_ai(int board[8][8], int player, int steps)
{
     int *valid = (int*)malloc(BRD_WIDTH*BRD_HEIGHT*sizeof(int));
     int valid_cnt;
     get_valid(board, player, valid, &valid_cnt);
     srand((unsigned int)time(NULL));
     if (valid_cnt == 0)
     {
          int i, j;
          for (i=0; i<8; i++)
          {
               for (j=0; j<8; j++)
                    printf("%d ", board[i][j]);
               putchar('\n');
          }
     }
     assert(valid_cnt != 0);
     return valid[rand()%valid_cnt];
}



static void get_valid(int board[8][8], int player, int *valid, int *valid_cnt)
{
     *valid_cnt = 0;
     int x, y;
     for (x=0; x<BRD_HEIGHT; x++)
     {
          for (y=0; y<BRD_WIDTH; y++)
          {
               if (is_valid(board, player, x*8+y))
               {
                    valid[*valid_cnt] = x*8 + y;
                    (*valid_cnt)++;
               }
          }
     }
}


static int is_valid(int board[8][8], int player, int pos)
{
     int x = pos / 8, y = pos % 8;
     if (board[x][y] != BRD_BLANK)
          return 0;
     int d;
     for (d=0; d<8; d++)
     {
          int xx = x + dir[d][0];
          int yy = y + dir[d][1];
          int cnt = 0;
          while (in_board(xx, yy) && board[xx][yy] == !player)
          {
               xx += dir[d][0];
               yy += dir[d][1];
               cnt++;
          }
          if (in_board(xx, yy) && board[xx][yy] == player && cnt != 0)
               return 1;
     }
     return 0;
}


/* int main(int argc, char *argv[]) */
/* { */
/*      int board[8][8] = {{-1, -1, -1, -1, -1, -1, -1, -1}, */
/*                         {-1, -1, -1, -1, -1, -1, -1, -1}, */
/*                         {-1, -1, -1, -1, -1, -1, -1, -1}, */
/*                         {-1, -1, -1,  1,  0, -1, -1, -1}, */
/*                         {-1, -1, -1,  0,  1, -1, -1, -1}, */
/*                         {-1, -1, -1, -1, -1, -1, -1, -1}, */
/*                         {-1, -1, -1, -1, -1, -1, -1, -1}, */
/*                         {-1, -1, -1, -1, -1, -1, -1, -1}}; */
/*      printf("%d\n", easy_ai(board, 0, 0)); */
/*      return 0; */
/* } */
