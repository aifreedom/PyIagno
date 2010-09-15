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

%module ai

%{
#include "ai.h"
     %}

%typemap(in) int board[8][8] (int temp[$1_dim0][$1_dim1]) {
     int i, j;
     if (!PySequence_Check($input))
     {
          PyErr_SetString(PyExc_ValueError,"Expected a sequence");
          return NULL;
     }
     if (PySequence_Length($input) != $1_dim0)
     {
          PyErr_SetString(PyExc_ValueError,"X size mismatch. Expected $1_dim0 elements");
          return NULL;
     }
     for (i=0; i<$1_dim0; i++)
     {
          PyObject *o = PySequence_GetItem($input, i);
          if (PySequence_Check(o))
          {
               if (PySequence_Length(o) != $1_dim1)
               {
                    PyErr_SetString(PyExc_ValueError,
                                    "Y size mismatch. Expected $1_dim1 elements");
                    return NULL;
               }
               for (j=0; j<$1_dim1; j++)
               {
                    PyObject *p = PySequence_GetItem(o, j);
                    if (PyNumber_Check(p))
                         temp[i][j] = (int) PyInt_AsLong(p);
                    else
                    {
                         PyErr_SetString(PyExc_ValueError,
                                         "Sequence elements must be numbers");      
                         return NULL;
                    }
               }
               
          }
          else
          {
               PyErr_SetString(PyExc_ValueError,"Expected a sequence");
               return NULL;
          }
     }
     $1 = temp;
 }


%typemap(out) int {
     $result = Py_BuildValue("(i,i)", $1/8, $1%8);
 }


extern int easy_ai(int board[8][8], int player, int steps);
