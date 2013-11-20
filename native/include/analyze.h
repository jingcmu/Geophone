#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI        M_PI    /* pi to machine precision, defined in math.h */
#define TWOPI     (2.0*PI)
#define FFTSIZE   256      //fft窗口大小
#define STARTFREQ 20      //start freq of Filter
#define ENDFREQ   80      //end freq of Filter
#define FFT_flag  1
#define IFFT_flag -1
#define FILTERVALUE 0

int  getFFT(double data [], int nn , int isign );
long getPower(double array[], int size);
long getFFTPower(const int * args);
