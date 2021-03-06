#include "analyze.h"
/*  计算fft系数，
 data-传入的震动幅值
 nn-data长度，必须为2的幂
 isign控制fft方向，1为fft，0为ifft
 */

#define DEBUG
#undef  DEBUG
int getFFT(double data [], int size , int isign )
{
    int n, mmax, m, j, istep, i;
    double wtemp, wr, wpr, wpi, wi, theta;
    double tempr, tempi;
    
    n = size << 1;
    j = 1;
    for (i = 1; i < n; i += 2) {
        if (j > i) {
            tempr = data[j];     data[j] = data[i];     data[i] = tempr;
            tempr = data[j+1]; data[j+1] = data[i+1]; data[i+1] = tempr;
        }
        m = n >> 1;
        while (m >= 2 && j > m) {
            j -= m;
            m >>= 1;
        }
        j += m;
    }
    mmax = 2;
    while (n > mmax) {
        istep = 2*mmax;
        theta = TWOPI/( isign*mmax);
        wtemp = sin(0.5*theta);
        wpr = -2.0*wtemp*wtemp;
        wpi = sin(theta);
        wr = 1.0;
        wi = 0.0;
        for (m = 1; m < mmax; m += 2) {
            for (i = m; i <= n; i += istep) {
                j =i + mmax;
                tempr = wr* data[j]   - wi* data[j+1];
                tempi = wr* data[j+1] + wi* data[j];
                data[j]   = data[i]   - tempr;
                data[j+1] = data[i+1] - tempi;
                data[i] += tempr;
                data[i+1] += tempi;
            }
            wr = (wtemp = wr)*wpr - wi*wpi + wr;
            wi = wi*wpr + wtemp*wpi + wi;
        }
        mmax = istep;
    }
    if(isign == IFFT_flag){
        for(i=0; i<size; i++){
            data[i*2+1] /= FFTSIZE;
            //虚部置为0
            data[i*2+2] = 0;
        }
    }
    return 0;
}

//带通滤波器，from startFreq to endFreq
void filter(double array[], int startFreq, int endFreq, double threshold){
    int i;
    for(i=0; i<(int)FFTSIZE*startFreq/SAMPLE_RATE; i++){
        array[(FFTSIZE-1-i)*2+1] = array[(FFTSIZE-1-i)*2+2] = array[i*2+1] = array[i*2+2] = threshold;
    }
    for(i=(int)FFTSIZE*endFreq/SAMPLE_RATE; i<FFTSIZE/2; i++){
        array[(FFTSIZE-1-i)*2+1] = array[(FFTSIZE-1-i)*2+2] = array[i*2+1] = array[i*2+2] = threshold;
    }
    return;
}

long getPower(double array[], int size){
    int i;
    long power = 0;
    for(i=0; i<size; i++){
        //fft系数求模并累加
        power += sqrt(array[i*2+1]*array[i*2+1]+array[i*2+2]*array[i*2+2]);
    }
    return power;
}
#ifdef DEBUG
void printData(double array[], int size){
    int i;
    for(i=0; i<size; i++){
        printf("%d:%f ", i, array[i*2+1]);
        printf("%d:%f ", i, array[i*2+2]);
    }
    printf("\n\n");
    return;
}
#endif

/* 计算fft系数和fft能量
 */
long getFFTPower(const int *args) {
    int i;
    long power = 0;
    double array[FFTSIZE*2+1];
#ifdef DEBUG
    printf("raw:\n");
#endif
    for(i=0; i<FFTSIZE; i++){
        array[2*i+1] = (double)args[i];
        array[2*i+2] = (double)0;
#ifdef DEBUG
        printf("%f ", array[2*i+1]);
        printf("%f ", array[2*i+2]);
#endif
    }
	getFFT(array, FFTSIZE, FFT_flag);
    filter(array, STARTFREQ, ENDFREQ, FILTERVALUE);
#ifdef DEBUG
    printf("\nFFT:\n");
    printData(array, FFTSIZE);
#endif
    getFFT(array, FFTSIZE, IFFT_flag);
#ifdef DEBUG
    printf("IFFT:\n");
    printData(array, FFTSIZE);
#endif
    power = getPower(array, FFTSIZE);
    return power;
}




