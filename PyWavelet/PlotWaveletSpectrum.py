import numpy as np
import wavelets
import matplotlib.pyplot as plt
from Plotting.PlotGrid import PlotGrid
from .GetWaveletObject import GetWaveletObject
from .WaveletPeaks import WaveletPeaks

def PlotWaveletPeriodogram(t,x,fig=None,maps=[1,1,0,0],wavelet='Morlet',ShowPeaks=True,Threshold=0.0):
	W = GetWaveletObject(t,x,wavelet)
	p = W.fourier_periods
	t = W.time

	dp = p[1:]-p[:-1]
	dt = t[1:]-t[:-1]
	
	paxis = np.append(p[0]-dp[0]/2,p[:-1]+dp/2)
	paxis = np.append(paxis,p[-1]+dp[-1]/2)
	
	taxis = np.append(t[0]-dt[0]/2,t[:-1]+dt/2)
	taxis = np.append(taxis,t[-1]+dt[-1]/2)
	
	Pow = W.wavelet_power
	if fig is None:
		fig = plt
		fig.figure()
		
	PlotGrid(fig,Pow.T,taxis,paxis,maps=maps,cmap=plt.cm.get_cmap('gnuplot'))
	if ShowPeaks:
		si,ti,grid = WaveletPeaks(Pow,Threshold)
		pp = p[si]
		tp = t[ti]
		plt.scatter(tp,pp,color=[0.0,1.0,0.0],zorder=10)


def PlotWaveletSpectrum(tin,x,fig=None,maps=[1,1,0,0],wavelet='Morlet',ShowPeaks=True,Threshold=0.0,UTisHours=False,zlog=True):
	T = tin.copy()
	if UTisHours:
		T*=3600.0
	bad = np.where(np.isfinite(x) == False)[0]
	x[bad] = 0.0
	W = GetWaveletObject(T,x,wavelet)
	f = 1.0/W.fourier_periods
	t = W.time

	df = f[1:]-f[:-1]
	dt = t[1:]-t[:-1]
	
	faxis = np.append(f[0]-df[0]/2,f[:-1]+df/2)
	faxis = np.append(faxis,f[-1]+df[-1]/2)
	
	taxis = np.append(t[0]-dt[0]/2,t[:-1]+dt/2)
	taxis = np.append(taxis,t[-1]+dt[-1]/2)
	
	if UTisHours:
		taxis/=3600.0
	
	Pow = W.wavelet_power.T
	Power = Pow.copy()
	Power[bad,:] = np.nan
	print(bad)
	if fig is None:
		fig = plt
		fig.figure()
		
	if zlog:
		Power = np.log10(Power)
	PlotGrid(fig,Power,taxis,faxis,maps=maps,cmap=plt.cm.get_cmap('gnuplot'))
	if ShowPeaks:
		si,ti,grid = WaveletPeaks(Pow.T,Threshold)
		fp = f[si]
		tp = t[ti]
		if UTisHours:
			tp/=3600.0
		plt.scatter(tp,fp,color=[0.0,1.0,0.0],zorder=10)
