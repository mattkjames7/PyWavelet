
all: o so

o:
	g++ -c -fpic Convolve.cc fft.cc ConvertComplex.cc

so:
	g++ -shared -o libconv.so Convolve.o fft.o ConvertComplex.o -lm
	
clean:
	rm -v *.o *.so
