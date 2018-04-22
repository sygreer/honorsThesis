#!/usr/bin/env python2

from solve import *

from numpy import empty, linspace, concatenate, pi, pad
from numpy.linalg import pinv, norm
from scipy.signal import butter, filtfilt, freqz
from scipy import fft, arange
import matplotlib.pyplot as plt

def main():
    print('Triange smoothing')
    print('functions include...')
    print('    foldConv(signal, filt)')
    print('    foldConvOp(triOper, sl)')
    print('    triOper(rect)')
    print('    lowPassFilter(data, highcut, fs, order, plot)')
    print('    plotSpec(y,Fs,col="red")')

def foldConv(signal,filt):
    """ 1D convolution with folding """
    
    # length of arrays and center
    fl = len(filt)
    sl = len(signal)
    center = int(len(filt)/2)

    # initialize convolved signal
    conv = [0]*sl

    # filter must be smaller than signal
    if fl > sl:
        raise ValueError, "Filter longer than signal"
    
    # convolve
    for i in range(0,sl):
        # center
        conv[i] += filt[center]*signal[i]

        # left
        for j in range(0,center):
            idx = abs(i-center+j)
            conv[i] += filt[j]*signal[idx]
            
        # right 
        for j in range(center + 1, fl):
            idx = i+j-center
            if idx >= sl:
                idx = (sl-1) - (idx - (sl-1))
            conv[i] += filt[j]*signal[idx]

    return conv

def foldConvOp(triOper, sl, plot=False):
    """ 1D convolution with folding """
    
    # length of arrays and center
    fl = len(triOper)
    center = int(fl/2)

    # initialize convolved signal
    conv = [0]*sl
    mat = empty([sl,sl])

    # filter must be smaller than signal
    if fl > sl:
        raise ValueError, "Filter longer than signal"
    
    # convolve
    for i in range(0,sl):
        # center
        mat[i,i] += triOper[center]

        # left
        for j in range(0,center):
            idx = abs(i-center+j)
            mat[i,idx] += triOper[j]
            
        # right 
        for j in range(center + 1, fl):
            idx = i+j-center
            if idx >= sl:
                idx = (sl-1) - (idx - (sl-1))
            mat[i,idx] += triOper[j]

    if plot: # plot the matrix
        plt.imshow(mat)
        plt.title("Forward operator")
        plt.show()

    return mat

def triOper(rect):
    """ create triangle smoothing operator """
    if rect < 1:
        raise ValueError, "Rect minimum size 1"

    # create triangle operator
    t = linspace(1,rect-1,rect-1)
    trian = concatenate((t,[rect],t[::-1]),axis=0)
    # normalize and return
    return trian/norm(trian)

def lowPassFilter(data, highcut, fs, order=5, plot=True):
    nyq = 0.5 * fs
    high = highcut / nyq

    b, a = butter(order, high, btype='lowpass')
    y = filtfilt(b, a, data) # zero phase
    w, h = freqz(b, a)

    if plot:
        plt.plot(w*fs/(2*pi), abs(h), 'b')
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency (Hz)')
        plt.title('Filter transfer function')
        plt.xlim([-5,120])
    return y

def plotSpec(y,Fs,col="red"):
    n = 5000
    y = pad(y, n, 'constant', constant_values=0) # increase resolution
    n = len(y) 
    k = arange(n)
    T = n/Fs
    frq = k/T 
    frq = frq[range(n/2)] 

    Y = fft(y)/n 
    Y = Y[range(n/2)]
    
    plt.plot(frq,abs(Y)/max(abs(Y)),col) 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectra')


if __name__ == "__main__":
    main()
