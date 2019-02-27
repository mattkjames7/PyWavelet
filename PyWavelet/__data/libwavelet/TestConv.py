import numpy as np
import ctypes
import time 

lib = ctypes.CDLL('./libconv.so')
CppConv = lib.Convolve
CppConv.argtypes = [	np.ctypeslib.ndpointer(ctypes.c_double,flags='C_CONTIGUOUS'),
						ctypes.c_int,
						np.ctypeslib.ndpointer(ctypes.c_double,flags='C_CONTIGUOUS'),
						ctypes.c_int,
						np.ctypeslib.ndpointer(ctypes.c_double,flags='C_CONTIGUOUS')]

_FFTConvolve = lib.FFTConvolve
_FFTConvolve.argtypes = [ctypes.c_int, np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS")]
_FFTConvolve.restype = None
_FFTConvolveN = lib.FFTConvolveNew
_FFTConvolveN.argtypes = [ctypes.c_int, np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS")]
_FFTConvolveN.restype = None


_FFT = lib.FFT
_FFT.argtypes = [ctypes.c_int, np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS"), np.ctypeslib.ndpointer(ctypes.c_double,flags="C_CONTIGUOUS")]
_FFT.restype = None


def TestFFT(i=32):
	x = np.random.rand(i)
	_N = np.int32(i)
	_xr = np.array(x).astype("float64")
	_xi = np.zeros(i,dtype="float64")
	_fr = np.zeros(i,dtype="float64")
	_fi = np.zeros(i,dtype="float64")
	
	_FFT(_N,_xr,_xi,_fr,_fi)

	npf = np.fft.fft(_xr)
	print(_xr)
	print(npf.real)
	return _xr,npf.real

def ZeroPad(x,n,Beginning=True):

	l = np.size(x)
	xi = np.copy(x)
	if l > n:
		print('Array cannot be zero-padded')
		return xi
	
	xo = np.zeros(n,dtype=xi.dtype)
	if Beginning:
		xo[0:l] = xi
	else:
		i0 = (n-l)//2
		xo[i0:i0+l] = xi
	return xo


def FFTConvolve(a, b, mode='full'):
	start_time=time.time()
	a = np.copy(a)
	b = np.copy(b)

	#zero pad first
	n = a.size
	m = b.size
	N = m + n -1
	a = ZeroPad(a,N)
	b = ZeroPad(b,N)
	

	#Convert input variables to appropriate numpy dtype:
	_N = np.int32(N)
	_a = np.array(a).astype("float64")
	_b = np.array(b).astype("float64")
	_c = np.zeros(N,dtype="float64")
	
	dt = time.time() - start_time
	#print('FFTConv Init:  ',dt)
	start_time=time.time()
	
	_FFTConvolve(_N, _a, _b, _c)

	dt = time.time() - start_time
	#print('FFTConv Run:  ',dt)
	start_time=time.time()

	if mode == 'full':
		return _c
	elif mode == 'same':
		l = np.max([n,m])
	else:
		l = np.max([n,m]) - np.min([n,m]) + 1
		
	out = _c[(N-l)//2:(N-l)//2+l]
	dt = time.time() - start_time
	#print('FFTConv Out:  ',dt)
	return out
	
	
def FFTConvolveNew(a, b, mode='full'):
	start_time=time.time()
	a = np.copy(a)
	b = np.copy(b)

	#zero pad first
	n = a.size
	m = b.size
	N = m + n -1
	a = ZeroPad(a,N)
	b = ZeroPad(b,N)
	

	#Convert input variables to appropriate numpy dtype:
	_N = np.int32(N)
	_a = np.array(a).astype("float64")
	_b = np.array(b).astype("float64")
	_c = np.zeros(N,dtype="float64")
	
	dt = time.time() - start_time
	print('FFTConvNew Init:  ',dt)
	start_time=time.time()
	
	_FFTConvolveN(_N, _a, _b, _c)

	dt = time.time() - start_time
	print('FFTConvNew Run:  ',dt)
	start_time=time.time()

	if mode == 'full':
		return _c
	elif mode == 'same':
		l = np.max([n,m])
	else:
		l = np.max([n,m]) - np.min([n,m]) + 1
		
	out = _c[(N-l)//2:(N-l)//2+l]
	dt = time.time() - start_time
	print('FFTConvNew Out:  ',dt)
	return out

def Conv(in1,in2):
	
	if np.size(in1) > np.size(in2):
		A = in1
		B = in2 
	else:
		A = in2
		B = in1
	
	nA = np.size(A)
	nB = np.size(B)
	
	aR = [0,0]
	bR = [0,0]
	
	out=np.zeros(nA,dtype='float64')
	
	for i in range(0,nA):
		aR[0] = np.max([0,i-nB//2])
		aR[1] = np.min([nA-1,i+nB//2-(nB+1)%2])
		bR[0] = np.max([0,nB//2-i])
		bR[1] = np.min([nB-1,nB//2+(nA-1-i)])

		tmp = 0.0
		nJ = aR[1]-aR[0]+1
		for j in range(0,nJ):
			tmp += A[aR[0]+j]*B[bR[0]+j]
			
		out[i] = tmp
		
	return out

def C_Conv(a,b):
	
	a = np.asarray(a,dtype='float64')
	na = np.int32(a.size)
	b = np.asarray(b,dtype='float64')
	nb = np.int32(b.size)
	out = np.zeros(np.max([na,nb]),dtype='float64')
	
	CppConv(a,na,b,nb,out)
	
	return out
	
	
def TestConv(na=15,nb=5):
	
	a = np.random.rand(na)
	b = np.random.rand(nb)
	
	start_time=time.time()
	o = np.convolve(a,b,'same')
	dt = time.time() - start_time
	print('Numpy: ',dt)
	start_time=time.time()
	o = FFTConvolve(a,b,'same')
	dt = time.time() - start_time
	print('FFTConv:  ',dt)
	start_time=time.time()
	o = FFTConvolveNew(a,b,'same')
	dt = time.time() - start_time
	print('FFTConvNew:  ',dt)
	start_time=time.time()
	o = C_Conv(a,b)
	dt = time.time() - start_time
	print('C_Conv:',dt)

