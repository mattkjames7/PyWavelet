#ifndef __Convolve_h__
#define __Convolve_h__
#include <stdio.h>
#include <complex.h>
#include "fft.h"
#include "ConvertComplex.h"
using namespace std;
#endif

extern "C" {
    void Convolve(double *a, int na, double *b, int nb, double *out);
    void _FFTConvolve(int N, double _Complex *a, double _Complex *b, double _Complex *c);
    void FFTConvolve(int N, double *a, double *b, double *c);
    void FFTConvolveNew(int N, double *a, double *b, double *c);
    void _FFTConvolveNew(int N, double _Complex *a, double _Complex *b, double _Complex *c);
}
