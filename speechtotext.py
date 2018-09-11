#for windows, pyaudio needs to be downloaded from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
#portaudio needs to be compiled like this. http://portaudio.com/docs/v19-doxydocs/compile_windows.html
#also portaudio needs to be downloaded compiled and placed in C:\Windows\System32
import pocketsphinx
import pyaudio
import wolframalpha
import pyglet
import gtts
import time
import speech_recognition as sr
from sentiment import *


WIT_AI_KEY=jd('localInfo.json')['witclientaccesstoken']
# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #print("sphinx thinks you said " + recognizer.recognize_sphinx(audio))
        #print(recognizer.recognize_sphinx(audio))
        print(recognizer.recognize_wit(audio,key=WIT_AI_KEY))
    except sr.UnknownValueError:
        #print("sphinx could not understand audio")
        pass
    except sr.RequestError as e:
        print("Could not request results from sphinx service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone(1)
def listen_print():
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    print("say something")
    while (True):
        with m as source:
            audio=r.listen(source, timeout=100, phrase_time_limit=10)
        callback(r,audio)

def transcribe(file):
    audio_file=relativepath(file)
    with sr.AudioFile(audio_file) as source:
        audio=r.record(source) 
    text=r.recognize_sphinx(audio)
    print(text)
listen_print()
# start listening in the background (note that we don't have to do this inside a `with` statement)
# stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
#for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
#while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stoppin

