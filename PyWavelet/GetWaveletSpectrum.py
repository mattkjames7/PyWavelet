import numpy as np
import wavelets
from .GetWaveletObject import GetWaveletObject
from .WaveletPeaks import WaveletPeaks

def GetWaveletSpectrum(tin,xin,wavelet='Morlet',GetPeaks=True,Threshold=0.0,UTisHours=False):
	T = tin.copy()
	if UTisHours:
		Tmult = 3600.0
	else:
		Tmult = 1.0
	x = xin.copy()
	bad = np.where(np.isfinite(x) == False)[0]
	x[bad] = 0.0
	W = GetWaveletObject(T*Tmult,x,wavelet)
	f = 1.0/W.fourier_periods
	t = W.time/Tmult

	df = f[1:]-f[:-1]
	dt = t[1:]-t[:-1]
	
	faxis = np.append(f[0]-df[0]/2,f[:-1]+df/2)
	faxis = np.append(faxis,f[-1]+df[-1]/2)
	
	taxis = np.append(t[0]-dt[0]/2,t[:-1]+dt/2)
	taxis = np.append(taxis,t[-1]+dt[-1]/2)
	

	Pow = W.wavelet_power.T
	Power = Pow.copy()
	Power[bad,:] = np.nan


		
	wlSpec = {}
	wlSpec['Power'] = Power
	wlSpec['F'] = f
	wlSpec['T'] = t
	wlSpec['Faxis'] = faxis
	wlSpec['Taxis'] = taxis	
	
	if GetPeaks:
		si,ti,grid = WaveletPeaks(Pow.T,Threshold)
		wlSpec['wlPeakF'] = f[si]
		wlSpec['wlPeakT'] = t[ti]
		wlSpec['wlPeakFind'] = si
		wlSpec['wlPeakTind'] = ti		
	
	return wlSpec
