import numpy as np
import wavelets

def GetWaveletObject(t,x,wavelet='Morlet'):
	
	if wavelet == 'Morlet':
		WL = wavelets.Morlet
	else:
		WL = wavelets.DOG
		
	dt = t[1]-t[0]
	W = wavelets.WaveletTransform(x,t,dt,wavelet=WL)
	return W
	
