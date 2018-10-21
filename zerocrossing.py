import numpy as np
import scipy.fftpack
import math
"""
the first objective is to change the given buffer to an array of zero crossing indexs 
"""
import matplotlib.pyplot as plt
import random
buffer = []
"""
for i in range (128):
    buffer.append(random.uniform(-1,1))
"""
N=44100
timeIntervals=1/44100
freq1=220
freq2=440
freq3=2750

for i in range(int(N)):
    buffer.append(np.sin(freq1*2*np.pi*i*timeIntervals)+0.5*np.sin(freq2*2*np.pi*i*timeIntervals)+0.25*np.sin(freq3*2*np.pi*i*timeIntervals))
"""
for i in range(int(N)):
    buffer.append(random.uniform(-1,1))
"""
"""
bufferf=scipy.fftpack.fft(buffer)
"""
bufferf=np.fft.fft(buffer)
xf=np.linspace(0.0 , 1/(2.0*timeIntervals), int(N/2))
yf=[]
for i in range (int(N/2)):
    yf.append(np.abs(bufferf[i]))



plt.plot(xf,yf)
plt.show()
def mstosamplelength(ms,sr=44100):
    return ms*sr/1000
def attackArray(attackMS):
    array=[0.0]
    attackLength=mstosamplelength(attackMS)
    for i in range(attackLength):
        array.append(math.log(1+(i)/attackLength)/math.log(2))
    return array
    
def decayArray(decayMS):
    decayLength=mstosamplelength(decayMS)
    array=[1.0]
    for i in range(decayLength-2):
        array.append(math.exp((-1*i)/(decayLength/10)))
    array.append(0.0)
    return array
def zero_crossing(buffer,samplerate):
    prvmax=0
    mx = 0
    sign = 1
    ahd = 'hold'
    prev_max=0
    max_index=0
    max_index_array= []
    length_array = 0
    zero_crossing_index_array=[]
    period_array = []
    ahd_array = []
    dictionary={}
    """
    need to think of ways to add hold (specifically 0 hold) in to consideration
    """
    for i in range(len(buffer)):
        if (np.sign(buffer[i])==0):
            length_array+=1
            if (np.sign(buffer[i])==sign):
                ahd="hold"
            else:
                sign=np.sign(buffer[i])
                zero_crossing_index_array.append(i)
                period_array.append(length_array)
                length_array = 0
                prev_max=mx
                mx=0

        else:
            if (np.sign(buffer[i])==sign):
                length_array+=1
                if(abs(buffer[i])>mx):
                    prev_max = mx
                    mx = abs(buffer[i])
                    max_index=i                    
                else:
                    pass

                if(prev_max>mx):
                    ahd = "attack"
                else:
                    ahd = "decay"

            else:
                max_index_array.append(max_index)
                sign=np.sign(buffer[i])
                zero_crossing_index_array.append(i)
                period_array.append(length_array)
                ahd_array.append(ahd)
                length_array=0
                prev_max=mx
                mx=buffer[i]
