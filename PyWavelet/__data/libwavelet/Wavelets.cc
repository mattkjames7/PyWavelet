#include "Wavelets.h"

double MorletFourierPeriod(double s,int w0) {
	return (4.0*M_PI*s)/(w0 + sqrt(2.0 + w0*w0));
}

double DoGFourierPeriod(double s, int m) {
	return (2.0*M_PI*s)/sqrt(m + 0.5);
}

void MorletFunction(int N, double *t, double s, int w0, double complex *o) {
	double x;
	double w = (double) w0;
	int i;
	for (i=0;i<N;i++) {
		x = t[i]/s;
		o[i] = (cexp(I*w*x) - exp(-0.5*(w*w)))*exp(-0.5*(x*x))*pow(M_PI,0.25); 
	}
}

	
