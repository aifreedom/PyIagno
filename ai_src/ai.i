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
     for (i=0; i<8; i++)
     {
          for (j=0; j<8; j++)
          {
               printf("%d ", temp[i][j]);
          }
          printf("\n");
     }     
     $1 = temp;
 }


%typemap(out) int {
     $result = Py_BuildValue("(i,i)", $1/8, $1%8);
 }


extern int easy_ai(int board[8][8], int player, int steps);
