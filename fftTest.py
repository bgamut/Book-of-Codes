import os
import scipy.io.wavfile as wav
import numpy as np
from numpy import convolve
from numpy.fft import fft,ifft
fname='/Users/bernardahn/Downloads/source.mp3'
oname='temp.wav'
cmd='lame --decode {0} {1}'.format(fname,oname)
os.system(cmd)
reference=wav.read(oname)

def split_fft(data):
    mono=np.arange(len(data[1]))
    monofft=np.arange(256)
    leftOnly=np.arange(len(data[1]))
    rightOnly=np.arange(len(data[1]))
    sidefft=np.arange(256)
    resultfftsq=np.zeros(shape=(256,2))
    for i in data[1]:
        a=(data[1][i][0]/2)/max(data[1].max(),data[1].min(),key=abs)
        #a=(data[1][i][0]/2)
        a.reshape((1,-1))
        b = (data[1][i][1]/2)/max(data[1].max(),data[1].min(),key=abs)
        #b = (data[1][i][1]/2)
        b.reshape((1,-1))
        mono[i]=a+b
        leftOnly[i]=a-b
        rightOnly[i]=b-a
    monofft=fft(mono,n=256)
    sidefft=fft(leftOnly,n=256)
    for i in monofft:
        a1=monofft[i][0]
        a2=monofft[i][1]
        a3=(a1*a1+a2*a2)*max(data[1].max(),data[1].min(),key=abs)
        b1=sidefft[i][0]
        b2=sidefft[i][1]
        b3=(b1*b1+b2*b2)*max(data[1].max(),data[1].min(),key=abs)
        resultfftsq[i]=[a3,b3]
    print("song analysis complete")
    return resultfftsq

def deconvolve(data,resultfftsq):
    mono=np.arange(len(data[1]))
    monofft=np.arange(256)
    leftOnly=np.arange(len(data[1]))
    rightOnly=np.arange(len(data[1]))
    sidefft=np.arange(256)
    ir=np.arange(256)
    for i in data[1]:
        a=(data[1][i][0]/2)/max(data[1].max(),data[1].min(),key=abs)
        #a=(data[1][i][0]/2)
        a.reshape((1,-1))
        b = (data[1][i][1]/2)/max(data[1].max(),data[1].min(),key=abs)
        #b = (data[1][i][1]/2)
        b.reshape((1,-1))
        mono[i]=a+b
        leftOnly[i]=a-b
        rightOnly[i]=b-a
    monofft=fft(mono,n=256)
    sidefft=fft(leftOnly,n=256)
    for i in monofft:
        a1=monofft[i][0]
        a2=monofft[i][1]
        a3=a1*a1+a2*a2
        b1=sidefft[i][0]
        b2=sidefft[i][1]
        b3=b1*b1+b2*b2
        c=(resultfftsq[0]/a3)*max(data[1].max(),data[1].min(),key=abs)
        d=(resultfftsq[1]/b3)*max(data[1].max(),data[1].min(),key=abs)
        ir[i]=[c,d]
    print("done with ir synthesis")
    return ir

def msconvolve(noise_data,ir):
    mono=np.arange(len(data[1]))
    leftOnly=np.arange(len(data[1]))
    rightOnly=np.arange(len(data[1]))
    
    for i in data[1]:
        #a=(data[1][i][0]/2)/max(data[1].max(),data[1].min(),key=abs)
        a=(data[1][i][0]/2)
        a.reshape((1,-1))
        #b = (data[1][i][1]/2)/max(data[1].max(),data[1].min(),key=abs)
        b = (data[1][i][1]/2)
        b.reshape((1,-1))
        mono[i]=a+b
        leftOnly[i]=a-b
        rightOnly[i]=b-a
    mono_convolve=convolve(mono,ir[0])/2
    left_convolve=convolve(leftOnly,ir[1])/2
    right_convolve=convolve(rightOnly,ir[1])/2
    result=np.zeros(shape=(2,len(mono_convolve)))
    for i in mono_convolve:
        result[i]=[left_convolve[i]+mono_convolve[i],right_convolve[i]+mono_convolve[i]]
    return result




reference_fft=np.zeros(shape=(256,2))
reference_fft=split_fft(reference)
red=wav.read("noise RED.wav")
print("red : "+str(red[1]))
print(str(split_fft(reference)))
redir=np.zeros(shape=(256,2))
redir=np.deconvolve(red,reference_fft)
redir=msconvolve(red,redir)
wav.write("redir.wav",44100,redir)
'''
brown=wav.read("noise BROWN.wav")
print("brown : "+str(brown[1]))
white=wav.read("noise WHITE.wav")
print("white : "+str(white[1]))
wav.write("brownir.wav",44100,brownir)
wav.write("whiteir.wav",44100,whiteir)
'''
