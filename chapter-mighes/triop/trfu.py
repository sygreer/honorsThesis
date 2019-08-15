#! /usr/bin/env python2

from triOp import *
import numpy as np
import matplotlib.pyplot as plt

# create an impulse
spike = np.zeros(100)
spike[50] = 1

# smooth spike to get impulse respnse of filter
rect = 10
tri = triOper(10)
smoo = foldConv(spike,tri)

# create filter
a = 1           # filter a term
fs = 1/0.001    # sampling frequency

# forward
w, h = freqz(smoo, a)

# inverse
w2, h2 = freqz(a, smoo)


# plot everything
fig, ax1 = plt.subplots()
ax1.set_title('Transfer functions, rect=%i samples, fs=%i Hz'%(rect,fs))
#ax1.set_title('Transfer functions')
ax1.plot(w*fs/(2*pi),  abs(h ), 'b')
ax1.set_ylim([0,4])
ax1.set_xlim([0,500])
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Forward', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
ax2.plot(w2*fs/(2*pi), abs(h2), 'r')
ax2.set_ylim([0,400])
ax2.set_ylabel('Inverse', color='r')
ax2.tick_params('y', colors='r')
fig.tight_layout()
#plt.show()
plt.savefig('Fig/tf.pdf', format='pdf', bbox_inches='tight')

