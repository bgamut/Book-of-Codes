print("")

print("Loading modules...")

from scipy.io import wavfile
from scipy import signal

"from scipy.fftpack import fft, ifft, rfft, fft2, ifft2"
import pyfftw
import numpy as np
import progressbar
import time
import pickle
import sys
from fbchat import Client
from fbchat.models import *
import twitter
import glob
import os
print ("Modules loaded.")

print("")

print("Loading functions...")

bins = 512
datatype = "float32"


def windowing(N):
    a = np.zeros((N, 1), "float32")
    for i in range(N):
        a[i] = 1 - np.cos(2 * np.pi * i / N)
    return a


"returns a window array of size N"


def gather(refTrack, bins=bins, datatype=datatype):
    "window=signal.gaussian(bins,7)"
    widgets = [
        '(', progressbar.ETA(), ')',
        progressbar.Bar(),
        '[', progressbar.Percentage(), ']',
    ]
    window = windowing(bins)
    length = int(refTrack.shape[0])
    itratio = length / bins
    "iterations = itratio * 2 - 1"
    iterations = itratio
    tempa = np.zeros((length, 1), datatype)
    tempb = np.zeros((bins, 1), 'complex128')
    tempc = np.zeros((bins, 2), datatype)
    refFft = np.zeros((bins, 1), "complex")
    print(" ")
    print("--part 1 of 2")
    with progressbar.ProgressBar(max_value=iterations, widgets=widgets) as bar1:
        for i in range(iterations):
            for j in range(bins):
                "index = i * bins / 2 + j"
                index = i*bins + j
                tempa[j] = refTrack[index]
                "tempa[j] = refTrack[index] * window[j]"

            tempb = np.fft.fft2(tempa)
            for k in range(bins):
                tempc[k][0] += np.abs(float(tempb[k].real[0])) / float(iterations)
                tempc[k][1] += np.abs(float(tempb[k].imag[0])) / float(iterations)

            bar1.update(i)
    time.sleep(15)
    print(" ")
    print("--part 2 of 2")
    """
    with progressbar.ProgressBar(max_value=iterations, widgets=widgets) as bar:
        for l in range(bins):
            refFft[l]=np.complex(tempc[l][0],tempc[l][1])
            bar.update(i)
            print(str(l) + "/" + str(bins-1))
    """
    with progressbar.ProgressBar(max_value=bins, widgets=widgets) as bar2:
        for l in range(bins):
            refFft[l] = np.complex(tempc[l][0], tempc[l][1])
            "print(str(l) + '/' + str(bins-1))"
            bar2.update(l)

    "ref=np.fft.ifft2(refFft)"
    print("refFft size : " + str(refFft.shape[0]))
    return refFft


"returns reference fft array of binsize=bins given a raw reference sample array"


def ferment(data, filepath):
    output = open(filepath, 'wb')
    pickle.dump(data, output)
    output.close()


"Saves data object to filepath"


def eat(filepath):
    picklefile = open(filepath, 'rb')
    data = pickle.load(picklefile)
    return data


"Returns fermented data from filepath"


def morph(original_FFT, ref_FFT):
    widgets = [
        '(', progressbar.ETA(), ')',
        progressbar.Bar(),
        '[', progressbar.Percentage(), ']',
    ]

    originalLength = int(original_FFT.shape[0])
    refFftLength = int(ref_FFT.shape[0])
    if (originalLength == refFftLength):
        for i in range(originalLength):
            ref_amp = float(np.power(float(ref_FFT.real[i]), 2)) + float(np.power(float(ref_FFT.imag[i]), 2))
            original_amp = float(np.power(float(original_FFT.real[i]),2)) + float(np.power(float(original_FFT.imag[i]),2))
            ratio=np.abs(ref_amp/original_amp)
            """
            "hypotenuse"
            
            h = float(np.power(refamp, 0.5))

            "adjacent"
            rv = float(originalFft.real[i])

            "opposite"
            iv = float(originalFft.imag[i])

            "phase"
            if (rv == 0.0):
                newR = 0.0
                newI = h
            elif (iv == 0.0):
                newR = h
                newI = 0.0
            else:
                phi = float(np.arctan2(rv, iv))
                newR = h * float(np.sin(phi))
                newI = h * float(np.cos(phi))
            """
            """
            amp=float(np.power(float(refFft[i].real[0]),2))+float(np.power(float(refFft[i].imag[0]),2))
            rs=float(np.power(float(original[i].real[0]),2))
            """
            """
            d=amp-rs
            n=float(np.power(d,0.5))
            original[i]=np.complex(float(original[i].real[0]),n)
            """

            original_FFT[i] = np.complex(float(original_FFT[i].real[0])*ratio,float(original_FFT[i].imag[0])*ratio)

        return original_FFT
    else:
        print('The length of the two input arrays do not match')
        print('original : ' + str(int(original_FFT.shape[0])))
        print('reference : ' + str(int(ref_FFT.shape[0])))


"returns updated original array. Changes the original signal fft's imaginary number according to ref's fft amplitude"


def fear(raw, refFft, bins=bins, datatype=datatype):
    widgets = [
        '(', progressbar.ETA(), ')',
        progressbar.Bar(),
        '[', progressbar.Percentage(), ']',
    ]
    window = windowing(bins)
    fullLength = int(raw.shape[0])
    itratio = fullLength / bins
    iterations = itratio * 2 - 1
    tempa = np.zeros((bins, 1), datatype)
    tempc = np.zeros((bins, 2), datatype)
    newTrack = np.zeros((fullLength, 1), datatype)
    with progressbar.ProgressBar(max_value=iterations, widgets=widgets) as bar:
        for i in range(iterations):
            print(str(i) + '/' + str(iterations))
            for j in range(bins):
                tempa[j] = raw[i * bins / 2 + j] * window[j]
            tempb = np.fft.fft2(tempa)
            morph(tempb, refFft)
            tempc = np.fft.ifft2(tempb).real
            for k in range(bins):
                newTrack[i * bins / 2 + k] += tempc[j]

        bar.update(i)

    print('rawFft size : ' + str(tempb.shape[0]))
    print(' ')
    print(' ')
    return newTrack


"returns new track. Changes the raw sample array to fit the refFft."


def original_track_copy(original_wav, bins=bins, datatype=datatype):
    widgets = [
        '(', progressbar.ETA(), ')',
        progressbar.Bar(),
        '[', progressbar.Percentage(), ']',
    ]
    original = wavfile.read(original_wav)
    originalsamplerate = original[0]
    originaldatatype = str(original[1].dtype)
    raw = original[1]
    rawlen = len(original[1])
    rawlength = rawlen - (rawlen % bins) + bins
    rawcopy = np.zeros((rawlength, 2), datatype)
    rawmono = np.zeros((rawlength, 1), datatype)
    rawleftonly = np.zeros((rawlength, 1), datatype)
    rawrightonly = np.zeros((rawlength, 1), datatype)

    print("Initiating original track raw sound array copy sequence...")
    with progressbar.ProgressBar(max_value=rawlen, widgets=widgets) as bar:
        for i in range(rawlen):
            rawcopy[i][0] = raw[i][0]
            rawcopy[i][1] = raw[i][1]
            rawmono[i] = (raw[i][0] / 2.0) + (raw[i][1] / 2.0)
            rawleftonly[i] = raw[i][0] - rawmono[i]
            rawrightonly[i] = raw[i][1] - rawmono[i]
            bar.update(i)

    "time.sleep(15)"
    print("Complete!")
    print("")
    return rawleftonly, rawrightonly, rawmono, rawlen, originalsamplerate, originaldatatype


"returns rawleftonly, rawrightonly, rawmono, rawlen, originalsamplerate, originaldatatype"


def reference_fft(referenceTrack, bins=bins, datatype=datatype):
    print("Initiating reference track raw sound array copy sequence...")

    widgets = [
        '(', progressbar.ETA(), ')',
        progressbar.Bar(),
        '[', progressbar.Percentage(), ']',
    ]
    reference = wavfile.read(referenceTrack)
    ref = reference[1]
    reflen = len(reference[1])
    reflength = reflen - (reflen % bins) + bins
    refsamplerate = reference[0]
    refdatatype = str(ref.dtype)
    refleftonly = np.zeros((reflength, 1), datatype)
    refrightonly = np.zeros((reflength, 1), datatype)
    refmono = np.zeros((reflength, 1), datatype)
    refcopy = np.zeros((reflength, 2), datatype)
    refleftOnlyFft = np.zeros((bins, 1), datatype)
    refrightOnlyFft = np.zeros((bins, 1), datatype)
    refmonoFft = np.zeros((bins, 1), datatype)
    with progressbar.ProgressBar(max_value=reflen, widgets=widgets) as bar:
        for i in range(reflen):
            refmono[i] = (ref[i][0] / 2.0) + (ref[i][1] / 2.0)
            refleftonly[i] = ref[i][0] - refmono[i]
            refrightonly[i] = ref[i][1] - refmono[i]
            bar.update(i)
    "time.sleep(15)"
    print("Complete!")
    print("")
    print("Initiating reference fft analysis sequence...")
    print("Analysis 1/3")
    refleftOnlyFft = gather(refleftonly, bins, datatype)
    "time.sleep(15)"
    print("Analysis 2/3")
    refrightOnlyFft = gather(refrightonly, bins, datatype)
    "time.sleep(15)"
    print("Analysis 3/3")
    refmonoFft = gather(refmono, bins, datatype)
    "time.sleep(15)"
    print("Complete!")
    print("")
    print(" ")
    return refleftOnlyFft, refrightOnlyFft, refmonoFft, refsamplerate, refdatatype


":returns refleftOnlyFft, refrightOnlyFft, refmonoFft, refsamplerate, refdatatype"

"""
todo: 

'check the datatype of original vs reference track and change the track needed updates to be updated'
def update_value(value,datatypein,datatypeout):
    return new_value

def update_array(array,sampleratein,samplerateout):
    return new_array
"""


def morph_all_channels(rawleftonly, rawrightonly, rawmono, refleftonlyfft, refrightonlyfft, refmonofft, bins=bins,
                       datatype=datatype):
    print("Initiating original track morphing sequence...")
    print("Morph 1/3")
    masterleftonly = fear(rawleftonly, refleftonlyfft, bins, datatype)
    time.sleep(15)
    print("Morph 2/3")
    masterrightonly = fear(rawrightonly, refrightonlyfft, bins, datatype)
    time.sleep(15)
    print("Morph 3/3")
    mastermono = fear(rawmono, refmonofft, bins, datatype)
    time.sleep(15)
    print("Complete!")
    return masterleftonly, masterrightonly, mastermono


"returns masterleftonly,masterrightonly,mastermono"


def master_print(filepath, masterleftonly, masterrightonly, mastermono, rawlen, samplerate, datatype=datatype):
    print("Printing Master Track to file")
    master = np.zeros((rawlen, 2), datatype)
    for i in range(rawlen):

        master[i][0] = mastermono[i]
        master[i][1] = mastermono[i]
        """
        master[i][0] = mastermono[i] + masterleftonly[i]
        master[i][1] = mastermono[i] + masterrightonly[i]
        """

    "wavfile.write('MASTER.wav',original[0],master)"
    wavfile.write(filepath, samplerate, master)
    time.sleep(15)
    print("Complete!")


"creates a master track at filepath. Filepath must consist the file name"
print('Functions loaded.')

print('')
def notify_me(message):
    client = Client('cumber86@hotmail.com','yS3-VQY-RzJ-8vr')
    client.send(Message(text=message), thread_id=client.uid, thread_type=ThreadType.USER)

def tweet(message):
    twit = twitter.Api(consumer_key="eOtFpo5JPUFFQZeVYxWciRj2Z",
                        consumer_secret="j7UDLedjqr5KRj9hrKHAe0vIKj82Gr3mWTFeprP583BmdBgsIt",
                        access_token_key="992221193225715712-npdxx2zwaJDeW6TVEa4v1OsqjTkl4Cr",
                        access_token_secret="f7sXT8Bn4SpErdO9eBGg3nSZvjRF6SSAGOnOPuCJtbw0d", input_encoding="utf-8")
    twit.PostUpdate(message)

def email_me(message):
    pass

"""
bins=512

reference = wavfile.read('reference.wav')
ref=reference[1]
reflen=len(reference[1])
reflength=reflen-(reflen%bins)+bins

original = wavfile.read('original.wav')
raw=original[1]
rawlen=len(original[1])
rawlength=rawlen-(rawlen%bins)+bins
datatype=reference[1].dtype


refleftonly=np.zeros((reflength, 1), datatype)
refrightonly=np.zeros((reflength, 1), datatype)
refmono=np.zeros((reflength, 1), datatype)
refcopy=np.zeros((reflength, 2), datatype)
refleftOnlyFft=np.zeros((bins,1), datatype)
refrightOnlyFft=np.zeros((bins,1), datatype)
refmonoFft=np.zeros((bins,1), datatype)

rawleftonly=np.zeros((rawlength, 1), datatype)
rawrightonly=np.zeros((rawlength, 1), datatype)
rawmono=np.zeros((rawlength, 1), datatype)
rawcopy=np.zeros((rawlength, 2), datatype)
rawleftOnlyFft=np.zeros((bins,1), datatype)
rawrightOnlyFft=np.zeros((bins,1), datatype)
rawmonoFft=np.zeros((bins,1), datatype)

master=np.zeros((rawlength,2), datatype)

widgets=[
    '(',progressbar.ETA(),')',
    progressbar.Bar(),
    '[', progressbar.Percentage(),']',
]
"""


def main(origTrack,ref_track,*args):
    """
    originalTrack=sys.argv[1]
    reference_track=sys.argv[2]
    filepath=sys.argv[3]
    """
    if(str(origTrack)==""):
        originalTrack = "original.wav"
    else:
        originalTrack = origTrack
    if (str(ref_track) == ""):
        reference_track = "reference.wav"
    else:
        reference_track = ref_track
    if(args):
        for arg in args:
            k=arg.split("=")[0]
            v=arg.split("=")[1]
            if(k=="data"):
                data=v
                print(data)
            else:
                data="test1024.db"
                print("x"+data)
            if(k=="filepath"):
                filepath=v
            else:
                filepath = "MASTER.wav"


    rawleftonly, rawrightonly, rawmono, rawlen, original_samplerate, original_datatype = original_track_copy(
        originalTrack)

    file_exists=False
    for file in glob.glob("*.db"):
        if str(file)==data:
            file_exists=True
    if (file_exists==False):
        refleftOnlyFft, refrightOnlyFft, refmonoFft, reference_samplerate, reference_datatype = reference_fft(
            reference_track)
        refdata = [refleftOnlyFft, refrightOnlyFft, refmonoFft, reference_samplerate, reference_datatype]
        ferment(refdata,data)
        notify_me("fermented")
    else :
        a=eat(data)
        refleftOnlyFft=a[0]
        refrightOnlyFft=a[1]
        refmonoFft=a[2]
        reference_samplerate=a[3]
        reference_datatype=a[4]


    masterleftonly, masterrightonly, mastermono = morph_all_channels(rawleftonly, rawrightonly, rawmono, refleftOnlyFft,
                                                                     refrightOnlyFft, refmonoFft)
    master_print(filepath, masterleftonly, masterrightonly, mastermono, rawlen, original_samplerate)
    "notify_me('test 1 complete and westworld season 2 is awesome')"
    "tweet('westworld season 2 is awesome!')"


if __name__ == "__main__":
    if len(sys.argv) ==1:
        main("", "", " = ")
    elif len(sys.argv) != 3:
        main(sys.argv[1],sys.argv[2],*sys.argv[3:])
    else:
        main(sys.argv[1],sys.argv[2])