CC = gcc
CFLAGS = -O2

.PHONY: all serial omp clean

all: serial omp

serial:
	$(CC) $(CFLAGS) -o stencil stencil.c

omp:
	$(CC) $(CFLAGS) -fopenmp -o stencil_omp stencil_omp.c

clean:
	rm -f stencil stencil_omp
