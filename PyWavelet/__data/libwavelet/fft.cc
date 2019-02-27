#include "fft.h"

void _fft(int n, double _Complex *buf, double _Complex *tmp, int step) {
	//this function does not work
	
	int i, j;
	double _Complex t;
	printf("n/step mod 2 : %d\n",((n/step) % 2));
	if ( ((n/step) % 2 > 0)) {
		/*this bit will do a simple DFT on the remaining values when there is an odd number left*/
		for (i=0;i<n;i+=step) {
			printf("DFT: %d %d %d\n",i,n,step);
			t = 0.0 + 0.0*I;
			for (j=0;j<n;j+=step) {
				t += cexp(-I*M_PI*i*j/n) * tmp[i + step-1];
			}
			buf[i] = tmp[i] + t;
		}
		
	} else if (step < n) {
		/*this should call the next _fft*/
		_fft(n, tmp, buf, step *2);
		_fft(n, tmp + step, buf + step, step *2);
		
		for (i=0;i<n;i+=2*step) {
			printf("FFT: %d %d %d\n",i,n,step);
			t = cexp(-I*M_PI*i/n) * tmp[i + step -1];
			buf[i/2] = tmp[i] + t;
			buf[(i+n)/2] = tmp[i] - t;
		}
	}
}

void FFT(int n, double *xinr, double *xini, double *Xoutr, double *Xouti) {
	/*this function will wrap around the nested function*/
	printf("1\n");
	/*copy input to complex buffer*/
	double _Complex buf[n], tmp[n];
	printf("2\n");
	DoubletoComplex(n,xinr,xini,buf);	
	printf("3\n");
	/*now to start the call to the actual fft algorithm*/
	_fft(n,buf,tmp,1);
	printf("4\n");
	/*convert ouput to double*/
	ComplextoDouble(n,buf,Xoutr,Xouti);
}
void FFT(int n, double _Complex *xin, double _Complex *Xout) {
	/*this function will wrap around the nested function*/
	
	/*copy input to complex buffer*/
	double _Complex buf[n], tmp[n];
	int i;
	for (i=0;i<n;i++) {
		buf[i] = xin[i];
	}
	
	/*now to start the call to the actual fft algorithm*/
	_fft(n,buf,tmp,1);
	
	for (i=0;i<n;i++) {
		Xout[i] = buf[i];
	}
}

void _ifft(int n, double _Complex *Xin) {
	double _Complex tmp[n], t;
	int i;
	
	_fft(n,Xin,tmp,1);
	Xin[0] = Xin[0]/n;
	for (i=1;i<(n/2+1);i++) {
		t= Xin[i];
		Xin[i] = Xin[n-i]/n;
		Xin[n-i] = t/n;
	}
	
}

void fft(int N, double _Complex *x, int stride, int offset) {
	double _Complex tmp[N];
	fft1(N,x,stride,offset,tmp);
}


void fft1(int N, double _Complex *x, int stride, int offset, double _Complex *tmp) {
	int i;
	double _Complex pi2N = -I*M_PI*2.0/N;
	if ((N % 2 > 0) || (N == 2)) {
		/* use discrete Fourier transform on what's left */
		int j;
		for (i=0;i<N;i++) {
			tmp[i] = 0.0 + I*0.0;
			for (j=0;j<N;j++) {
				tmp[i] += x[j*stride+offset]*cexp(pi2N*j*i); 
			}

		}
		for (i=0;i<N;i++) {
			x[stride*i+offset] = tmp[i];
		}
	} else {
		/* split x and call fft on odd and even parts of x*/
		int N2 = N/2;
		int stride2 = stride*2;
		
		fft1(N2,x,stride2,offset,tmp);
		fft1(N2,x,stride2,offset+stride,tmp);
		
		 
		for (i=0;i<N2;i++) {
			tmp[i] = x[stride2*i+offset] + cexp(pi2N*i)*x[stride2*i+stride+offset];
			tmp[i+N2] = x[stride2*i+offset] + cexp(pi2N*(i+N2))*x[stride2*i+stride+offset];
		}
		for (i=0;i<N;i++) {
			x[stride*i+offset] = tmp[i];
		}
	}
}


void ifft(int N, double _Complex *X) {
	double _Complex tmp;
	int i;
	
	fft(N,X,1,0);
	X[0] = X[0]/N;
	for (i=1;i<(N/2+1);i++) {
		tmp = X[i];
		X[i] = X[N-i]/N;
		X[N-i] = tmp/N;
	}
	
	
	
}
