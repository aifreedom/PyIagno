/* PyIagno - wxPython based implementation of a classial Reversi
 * game */

/* Copyright (C) 2010 aifreedom <me@aifreedom.com> */

/* PyIagno is free software; you can redistribute it and/or modify it */
/* under the terms of the GNU General Public License as published by */
/* the Free Software Foundation; either version 2 of the License, or */
/* (at your option) any later version. */

/* PyIagno is distributed in the hope that it will be useful, but */
/* WITHOUT ANY WARRANTY; without even the implied warranty of */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU */
/* General Public License for more details. */

/* You should have received a copy of the GNU General Public License */
/* along with PyIagno; if not, write to the Free Software Foundation, */
/* Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA */

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <assert.h>
#include <limits.h>
#include <string.h>
#include "ai.h"

#define MAX_DEPTH 7

#define BRD_WIDTH 8
#define BRD_HEIGHT 8
#define BRD_TOTAL BRD_WIDTH * BRD_HEIGHT

#define in_board(x, y) ((x)>=0 && (x)<BRD_HEIGHT && (y)>=0 && (y)<BRD_WIDTH)

#define MAX(x, y) ((x)>(y)?(x):(y))
#define MIN(x, y) ((x)<(y)?(x):(y))

#define get_x(pos) ((pos) >> 3)
#define get_y(pos) ((pos) & 0x7)

enum {BRD_BLANK=-1, BRD_DARK, BRD_LIGHT};

static void get_valid(int board[8][8], int player, int *valid, int *valid_cnt);
int validate(int board[8][8], int player, int pos, int flip);

// static void get_valid(int board[8][8], int player, int *valid, int *valid_cnt);
// static int is_valid(int board[8][8], int player, int pos);

const int dir[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1},
                       {1, -1}, {1, 0}, {1, 1}};

const float weight[6] = {10, 801.724, 382.026, 78.922, 74.396, 10};

const int V[8][8] = {{20, -3, 11, 8, 8, 11, -3, 20},
                     {-3, -7, -4, 1, 1, -4, -7, -3},
                     {11, -4, 2, 2, 2, 2, -4, 11},
                     {8, 1, 2, -3, -3, 2, 1, 8}, 
                     {8, 1, 2, -3, -3, 2, 1, 8}, 
                     {11, -4, 2, 2, 2, 2, -4, 11},
                     {-3, -7, -4, 1, 1, -4, -7, -3},
                     {20, -3, 11, 8, 8, 11, -3, 20}};

int corner[4][2] = {{0, 0}, {0, 7}, {7, 0}, {7, 7}};
int corner_close[12][2] = {{0, 1}, {1, 0}, {1, 1},
                          {0, 6}, {1, 6}, {1, 7},
                          {6, 0}, {6, 1}, {7, 1},
                          {6, 6}, {6, 7}, {7, 6}};

int total;

int easy_ai(int board[8][8], int player, int steps)
{
     int valid[BRD_TOTAL];
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

int frontier(int board[BRD_HEIGHT][BRD_WIDTH], int x, int y)
{
     int i;
     for (i=0; i<8; i++)
     {
          int xx = x + dir[i][0];
          int yy = y + dir[i][1];
          if (!in_board(xx, yy) || board[xx][yy] == BRD_BLANK)
               return 1;
     }
     return 0;
}



void calc(int board[BRD_HEIGHT][BRD_WIDTH], float val[6])
{
     int i, j, k, l, m;
     int dark, light;
     int valid[BRD_TOTAL];
     int dark_valid, light_valid;
     int dark_cor, light_cor;
     int dark_cor_close, light_cor_close;
     int dark_front, light_front;
     
     
     dark = light = 0;
     dark_cor = light_cor = 0;
     dark_cor_close = light_cor_close = 0;
     dark_front = light_front = 0;
     memset(val, 0, sizeof(float)*6);
     
     for (i=0; i<8; i++)
     {
          for (j=0; j<8; j++)
          {
               if (board[i][j] == BRD_DARK)
               {
                    dark++;
                    if (frontier(board, i, j))
                         dark_front++;
                    val[5] += V[i][j];
               }
               else if (board[i][j] == BRD_LIGHT)
               {
                    light++;
                    if (frontier(board, i, j))
                         light_front++;
                    val[5] -= V[i][j];
               }
          }
     }
     get_valid(board, BRD_DARK, valid, &dark_valid);
     get_valid(board, BRD_LIGHT, valid, &light_valid);

     // Piece difference
     if (dark == light)
          val[0] = 0;
     else if (dark > light)
          val[0] = 100 * ((float)dark / (dark + light));
     else
          val[0] = -100 * ((float)dark / (dark + light));
     
     // Corner occupancy
     for (i=0; i<4; i++)
     {
          int x = corner[i][0], y = corner[i][1];
          if (board[x][y] == BRD_DARK)
               dark_cor++;
          else if (board[x][y] == BRD_LIGHT)
               light_cor++;
     }
     val[1] = 25 * (dark_cor - light_cor);

     // Corner closeness
     for (i=0; i<12; i++)
     {
          int x = corner_close[i][0], y = corner_close[i][1];
          if (board[x][y] == BRD_DARK)
               dark_cor_close++;
          else if (board[x][y] == BRD_LIGHT)
               light_cor_close++;
     }
     val[2] = 12.5 * (light_cor_close - dark_cor_close);
     
     // Mobility
     if (dark_valid == light_valid ||
         dark_valid == 0 ||
         light_valid == 0)
          val[3] = 0;
     else if (dark_valid > light_valid)
          val[3] = 100 * ((float)dark_valid / (dark_valid + light_valid));
     else
          val[3] = -100 * ((float)light_valid / (dark_valid + light_valid));

     // Frontier discs
     if (dark_front == light_front)
          val[4] = 0;
     else if (dark_front > light_front)
          val[4] = -100 * ((float)dark_front / (dark_front + light_front));
     else
          val[4] = 100 * ((float)light_front / (dark_front + light_front));

}

static float eval(int board[8][8], int player)
{
     float c[6];
     float val = 0;
     int i, j;
     
     calc(board, c);
     
     for (i=0; i<6; i++)
          val += c[i] * weight[i];
     return val;
}


int validate(int board[8][8], int player, int pos, int flip)
{
     int x = pos / 8, y = pos % 8;
     if (!flip && board[x][y] != BRD_BLANK)
          return 0;
     if (flip && board[x][y] == BRD_BLANK)
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
          {
               if (!flip)
                    return 1;
               if (flip)
                    while (xx != x || yy != y)
                    {
                         board[xx][yy] = player;
                         xx -= dir[d][0];
                         yy -= dir[d][1];
                    }
          }
     }
     return 0;
}

void get_board(int board[8][8], int pos, int player, int next_board[8][8])
{
     int x = get_x(pos);
     int y = get_y(pos);
     int d;
     memcpy(next_board, board, sizeof(int)*BRD_TOTAL);
     next_board[x][y] = player;
     for (d=0; d<8; d++)
          validate(next_board, player, pos, 1);
}

static float minimax(int depth, int board[8][8], int player, int valid[], int valid_cnt, int *pos)
{
     if (depth == MAX_DEPTH)
          return eval(board, player);
     else
     {
          int next_valid[BRD_TOTAL];
          int next_valid_cnt;
          int next_board[BRD_HEIGHT][BRD_WIDTH];
          
          int value;     /* The value of current configuration */ 
          int tmp, i;    /* Local variables */
          int l_pos;
          
          if (player == BRD_DARK) value = INT_MIN;
          else value = INT_MAX;
          for (i=0; i<valid_cnt; i++)
          {
               get_board(board, valid[i], player, next_board);
               get_valid(next_board, !player, next_valid, &next_valid_cnt);
               tmp = minimax(depth+1, next_board, !player, next_valid, next_valid_cnt, &l_pos);
               
               /* Perform minimax algorithm */
               if ((tmp > value && player == BRD_DARK) ||
                   (tmp < value && player == BRD_LIGHT))
               {
                    value = tmp;
                    *pos = valid[i];
               }
          }
          return value;
     }
}

static float alpha_beta(int depth, int board[8][8], float alpha, float beta, int player, int valid[], int valid_cnt, int *pos)
{
     int next_valid[BRD_TOTAL];
     int next_valid_cnt;
     int next_board[BRD_HEIGHT][BRD_WIDTH];
          
     int value = INT_MIN;  /* The value of current configuration */ 
     int i;    /* Local variables */
     float tmp;
     int l_pos = 0;

     if (depth == 0)
          return eval(board, player);
     
     if (valid_cnt == 0) /* consider the end game */
     {
          get_valid(board, !player, next_valid, &next_valid_cnt);
          if (next_valid_cnt == 0)
               return eval(board, !player);
     }

     for (i=0; i<valid_cnt; i++)
     {
          if (alpha >= beta)
          {
               total++;
               break;
          }
          get_board(board, valid[i], player, next_board);
          get_valid(next_board, !player, next_valid, &next_valid_cnt);
          tmp = alpha_beta(depth-1, next_board, alpha, beta, !player, next_valid, next_valid_cnt, &l_pos);
          if (player == BRD_DARK && tmp > alpha) /* if max */
          {
               alpha = tmp;
               *pos = valid[i];
          }
          if (player == BRD_LIGHT && tmp < beta) /* if min */
          {
               beta = tmp;
               *pos = valid[i];
          }
     }

     if (player == BRD_DARK)
          return alpha;
     else
          return beta;
}


int medium_ai(int board[8][8], int player, int steps)
{
     int valid[BRD_TOTAL];
     int valid_cnt;
     int pos = 0;
     get_valid(board, player, valid, &valid_cnt);
     minimax(0, board, player, valid, valid_cnt, &pos);
     return pos;
}

int insane_ai(int board[8][8], int player, int steps)
{
     int valid[BRD_TOTAL];
     int valid_cnt;
     int pos = 0;
     get_valid(board, player, valid, &valid_cnt);
     total = 0;
     if (steps < 10)
          alpha_beta(9, board, INT_MIN, INT_MAX, player, valid, valid_cnt, &pos);
     else if (steps < 40)
          alpha_beta(7, board, INT_MIN, INT_MAX, player, valid, valid_cnt, &pos);
     else if (steps <= 60)
          alpha_beta(11, board, INT_MIN, INT_MAX, player, valid, valid_cnt, &pos);
     printf("%d cuts!\n", total);
     return pos;
}


static void get_valid(int board[8][8], int player, int *valid, int *valid_cnt)
{
     *valid_cnt = 0;
     int x, y;
     for (x=0; x<BRD_HEIGHT; x++)
     {
          for (y=0; y<BRD_WIDTH; y++)
          {
               if (validate(board, player, x*8+y, 0))
               {
                    valid[*valid_cnt] = x*8 + y;
                    (*valid_cnt)++;
               }
          }
     }
}
