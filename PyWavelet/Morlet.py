import numpy as np

def Morlet(t,s=1.0,w0=6.0):
	x = t/s
	out = (np.exp(1j*w0*x) - np.exp(-(w0**2)/2.0))*np.exp(-(x**2)/2.0)*np.pi**0.25
	return out


def MorletFreq(s=1.0,w0=6):
	return (w0 + np.sqrt(2.0 + w0*2))/(4.0*np.pi*s),w0/(2.0*np.pi*s)
