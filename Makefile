##################################################################
# Use SWIG to integrate hellolib.c for use in Python programs on
# Cygwin.  The SO must have a leading "_" in its name in current
# SWIG (>1.3.13) because also makes a .py without "_" in its name.
##################################################################

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

