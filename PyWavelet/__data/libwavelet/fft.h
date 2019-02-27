#ifndef __fft_h__
#define __fft_h__
#include <stdlib.h>
#include <stdio.h>
#include <complex.h>
#include <math.h>
#include "ConvertComplex.h"

using namespace std;
#endif

extern "C" {
	void fft(int N, double _Complex *x, int stride, int offset);
	void ifft(int N, double _Complex *X);
	void _fft(int n, double _Complex *x, double _Complex *tmp, int step);
	void _ifft(int n, double _Complex *Xin);
	void FFT(int n, double *xinr, double *xini, double *Xoutr, double *Xouti);
	void fft1(int N, double _Complex *x, int stride, int offset, double _Complex *tmp);

}
