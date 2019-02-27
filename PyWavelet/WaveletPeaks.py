import numpy as np

def WaveletPeaks(Pow,Threshold=0.0):
	
	grid = ((Pow[1:-1,1:-1] >= Pow[0:-2,1:-1]) & (Pow[1:-1,1:-1] >= Pow[2:,1:-1])) & ((Pow[1:-1,1:-1] >= Pow[1:-1,0:-2]) & (Pow[1:-1,1:-1] >= Pow[1:-1,2:])) & (Pow[1:-1,1:-1] >= Threshold)
	pgrid = np.zeros(Pow.shape,dtype='bool')
	pgrid[1:-1,1:-1] = grid
	si,ti = np.where(pgrid)
	
	return si,ti,pgrid
