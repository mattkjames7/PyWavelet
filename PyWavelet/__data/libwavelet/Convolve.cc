#include "Convolve.h"

void FFTConvolve(int N, double *a, double *b, double *c) {
	int i;
	double _Complex A[N], B[N], C[N];
	double z[N];
	for (i=0;i<N;i++) {
		z[i] = 0.0;
	}
	DoubletoComplex(N,a,z,A);
	DoubletoComplex(N,b,z,B);
	_FFTConvolve(N,A,B,C);
	ComplextoDouble(N,C,c,z);
}


void _FFTConvolve(int N, double _Complex *a, double _Complex *b, double _Complex *c) {
	int i;
	fft(N,a,1,0);
	fft(N,b,1,0);
	for (i=0;i<N;i++) {
		c[i] = a[i]*b[i];
	}
	ifft(N,c);
}
void FFTConvolveNew(int N, double *a, double *b, double *c) {
	int i;
	double _Complex A[N], B[N], C[N];
	double z[N];
	printf("1\n");
	for (i=0;i<N;i++) {
		z[i] = 0.0;
	}
	printf("2\n");
	DoubletoComplex(N,a,z,A);
	printf("3\n");
	DoubletoComplex(N,b,z,B);
	printf("4\n");
	_FFTConvolveNew(N,A,B,C);
	printf("5\n");
	ComplextoDouble(N,C,c,z);
}


void _FFTConvolveNew(int N, double _Complex *a, double _Complex *b, double _Complex *c) {
	int i;
	double _Complex *tmp;
	_fft(N,a,tmp,1);
	_fft(N,b,tmp,1);
	for (i=0;i<N;i++) {
		c[i] = a[i]*b[i];
	}
	_ifft(N,c);
}



void Convolve(double *a, int na, double *b, int nb, double *out) {
	double *A, *B;
	int nA, nB;
	int offset;
	if (na > nb) {
		A = a;
		B = b;
		nA = na;
		nB = nb;
	} else {
		A = b;
		B = a;
		nA = nb;
		nB = na;
	}		
	
	int i, j, aR[2], bR[2], C0, C1, C2, C3, C4, nj;
	C0 = nB/2;
	C1 = nA-1;
	C2 = C0-(nB+1)%2;
	C3 = nB-1;
	C4 = C0 + C1;
	double tmp;
	for (i=0;i<nA;i++) {
		aR[0] = max(0,i-C0);
		aR[1] = min(C1,i+C2);
		bR[0] = max(0,C0-i);
		bR[1] = min(C3,C4-i);
		tmp = 0.0;
		nj = aR[1]-aR[0]+1;
		for (j=0;j<nj;j++) {
			tmp += A[j+aR[0]]*B[j+bR[0]];
		}
		out[i] = tmp;
	}
}
