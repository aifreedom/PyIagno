# PyIagno - wxPython based implementation of a classial Reversi game

# Copyright (C) 2010 aifreedom <me@aifreedom.com>

# PyIagno is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.

# PyIagno is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

# You should have received a copy of the GNU General Public License
# along with PyIagno; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

PYLIB = /usr/bin
PYINC = /usr/include/python2.6
CLIB  = ai_src
PHONY = clean

# the library plus its wrapper
_ai.so: $(CLIB)/ai_wrap.o $(CLIB)/ai.o
	gcc -shared $(CLIB)/ai_wrap.o $(CLIB)/ai.o -L$(PYLIB) -lpython2.6 -o $@


# generated wrapper module code
$(CLIB)/ai_wrap.o: $(CLIB)/ai_wrap.c $(CLIB)/ai.h
	gcc $(CLIB)/ai_wrap.c -g -I$(CLIB) -I$(PYINC) -c -o $@

$(CLIB)/ai_wrap.c: $(CLIB)/ai.i
	swig -python -I$(CLIB) -outdir $(CLIB)/ $(CLIB)/ai.i
	mv $(CLIB)/ai.py .

# C library code (in another directory)
$(CLIB)/ai.o: $(CLIB)/ai.c $(CLIB)/ai.h
	gcc $(CLIB)/ai.c -g -I$(CLIB) -c -o $(CLIB)/ai.o

clean:
	rm -f *.so *.o *.pyc ai.py $(CLIB)/*.o $(CLIB)/*.pyc $(CLIB)/ai_wrap.c 

