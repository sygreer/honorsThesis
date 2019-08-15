#!/usr/bin/env python

from scipy.fftpack import fft
from numpy import linspace, concatenate, asarray, sin, cos, pi
from numpy.linalg import norm
import matplotlib.pyplot as plt

# fonts and such
bg_color = 'black'
fg_color = 'white'
fig = plt.figure(facecolor=bg_color, edgecolor=fg_color)
axes = plt.axes(facecolor=bg_color, frameon=True)

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

def triOper(rect):
    """ create triangle smoothing operator """
    if rect < 1:
        raise ValueError, "Rect minimum size 1"

    # create triangle operator
    t=linspace(1,rect-1,rect-1)
    trian = concatenate((t,[rect],t[::-1]),axis=0)

    # normalize and return
    return trian/norm(trian)

def sigPlot(name):
    fig.set_size_inches(10, 2)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)

    plt.ylim(ymin=-1.2, ymax=1.2)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    plt.savefig('Fig/%s'%name, format='pdf', bbox_inches='tight', 
                 transparent=True, dpi=200)

    plt.cla()

def freqPlot(signal, name, col):
    scale=20                    # freq scale
    smallTri = triOper(4)       # smoothing
    num = 5000                  # freq density

    Y = fft(signal, num)
    Y = Y[range(len(signal)/scale)]
    Y = foldConv(Y,smallTri)
    plt.plot(abs(Y/max(Y)), color=col)
    plt.xlabel("Frequency (Hz)")
    fig.set_size_inches(3, 2)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(True)
    axes.spines['left'].set_visible(True)
    axes.spines['bottom'].set_visible(True)
    plt.xticks([])
    plt.savefig(name, format='pdf', bbox_inches='tight', transparent=True, dpi=200)
    plt.cla()

def main():

    # read data and convert
    f = open('trace.txt', 'r')
    signal = f.readlines()
    signal = [y.strip() for y in signal]
    signal = map(float, signal)
    signal = asarray(signal)
    
    signal = signal[3900:5000]
    
    # create triangle operators
    tri = triOper(50)
    
    leg = foldConv(signal,tri)

    # time
    t = linspace(0,len(signal),len(signal))

    # amplitude
    amp = 0.1*sin(2*pi*t) - 0.2*cos(2*pi*2*t)
    t2 = t + 3*(1*sin(2*pi*t) - 4*cos(2*pi*2*t)+4)

    # plot everything 
    ########################################
    # display stuffs
    frame1 = plt.gca()
    frame1.axes.get_yaxis().set_visible(False)
    
    # plot color stuff -- white on black
    axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
    axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
    axes.xaxis.label.set_color(fg_color)
    axes.yaxis.label.set_color(fg_color)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    fig.set_size_inches(15, 4)
    frame1.axes.get_xaxis().set_visible(False)
    for spine in axes.spines.values():
        spine.set_color(fg_color)
    ########################################
    signal = signal / max(signal)
    signal = signal + amp
    leg = leg / max(leg)

    # time domain
    plt.plot(t, leg, color="black")
    plt.plot(t2, signal, color="red")
    sigPlot("bef.pdf")


    plt.plot(t, leg, color="black")
    plt.plot(t2, signal, color="red")
    sigPlot("one0.pdf")

    # BALANCE FREQ THEN AMP
    # balance freq
    sig2 = foldConv(signal,tri)
    sig2 = sig2 / max(sig2)

    plt.plot(t, leg, color="black")
    plt.plot(t2, sig2, color="red")
    sigPlot("one1.pdf")

    # balance amp
    ampBal = foldConv(leg,tri)
    ampBal = foldConv(ampBal,tri)
    ampBal = ampBal / (max(ampBal)*1.5)
    sig3 = sig2 + ampBal
    sig3 = sig3 / max(sig3)

    plt.plot(t, leg, color="black")
    plt.plot(t2, sig3, color="red")
    sigPlot("one2.pdf")

    # time shifts

    plt.plot(t, leg, color="black")
    plt.plot(t, sig3, color="red")
    sigPlot("one3.pdf")


    # BALANCE AMP THEN FREQ

    # balance amp
    ampBalb = foldConv(leg,tri)
    ampBalb = foldConv(ampBalb,tri)
    ampBalb = ampBalb / (max(ampBalb)*1.5)
    sigb2 = signal + ampBal
    sigb2 = sigb2 / max(sigb2)

    plt.plot(t, leg, color="black")
    plt.plot(t2, sigb2, color="yellow")
    sigPlot("two1.pdf")

    # balance freq
    sigb3 = foldConv(sigb2,tri)
    sigb3 = sigb3 / max(sigb3)

    plt.plot(t, leg, color="black")
    plt.plot(t2, sigb3, color="yellow")
    sigPlot("two2.pdf")

    # time shifts
    plt.plot(t, leg, color="black")
    plt.plot(t, sigb3, color="yellow")
    sigPlot("two3.pdf")

    #after
    plt.plot(t, leg, color="black")
    plt.plot(t, sig3, color="green")
    plt.plot(t, sigb3, color="yellow")
    sigPlot("aft.pdf")
    
if __name__ == "__main__":
    main()
