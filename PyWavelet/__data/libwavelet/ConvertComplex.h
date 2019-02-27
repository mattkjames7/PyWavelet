#ifndef __ConvertComplex_h__
#define __ConvertComplex_h__
#include <stdio.h>
#include <complex.h>
using namespace std;
#endif

void DoubletoComplex(int N, double *xr, double *xi, double _Complex *x);
void ComplextoDouble(int N, double _Complex *x, double *xr, double *xi);
