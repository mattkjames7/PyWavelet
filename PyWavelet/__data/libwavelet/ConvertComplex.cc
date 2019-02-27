#include "ConvertComplex.h"

void DoubletoComplex(int N, double *xr, double *xi, double _Complex *x) {
	int i;
	for (i=0;i<N;i++) {
		x[i] = xr[i] + xi[i]*I;
	}
}

void DoubletoComplex(int N, double *xr, double _Complex *x) {
	int i;
	for (i=0;i<N;i++) {
		x[i] = xr[i] + 0.0*I;
	}
}

void ComplextoDouble(int N, double _Complex *x, double *xr, double *xi) {
	int i;
	for (i=0;i<N;i++) {
		xr[i] = creal(x[i]);
		xi[i] = cimag(x[i]);
	}
} 
