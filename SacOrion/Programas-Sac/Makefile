FC=gfortran
# Activar todos advertencias y checks
FFLAGS=-g # instrument for debugging
FFLAGS+=-Wall -Wtabs # turn on all warnings (except allow literal TAB characters)
FFLAGS+=-fbounds-check 		# check array bounds
FFLAGS+=-ffpe-trap=invalid,zero,overflow # trap "serious" FP exceptions
FFLAGS+=-Wimplicit-procedure # warn about missing explicit interfaces

LDFLAGS=-L/usr/local/Cellar/cfitsio/3.350/lib -lcfitsio

all: PDF_2D_orion PDF_2D_orion2

%.o: %.f90
	$(FC) $(FFLAGS) -c $<

PDF_2D_orion: PDF_2D_orion.o wfitsutils.o 
	$(FC) $(FFLAGS) -o $@ $^ $(LDFLAGS)

PDF_2D_orion2: PDF_2D_orion2.o wfitsutils.o 
	$(FC) $(FFLAGS) -o $@ $^ $(LDFLAGS)
