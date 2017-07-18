import AutoTune
import pyo
class Autotune(pyo.PyoObject):
    def __init__(self, input, FS=44100.0,CHUNK=256,SCALE_ROTATE=0,LFO_QUANT=0,CONCERT_A=440.0,FIXED_PITCH=2.0,FIXED_PULL=0.1,CORR_STR=1.0,CORR_SMOOTH=0.0,PITCH_SHIFT=1.0,LFO_DEPTH=0.1,LFO_RATE=1.0,LFO_SHAPE=0.0,LFO_SYMM=0.0,FORM_WARP=0.0,MIX=1.0,KEY="c"):
        PyoObject.__init__(self,input,FS=44100.0,CHUNK=256,SCALE_ROTATE=0,LFO_QUANT=0,CONCERT_A=440.0,FIXED_PITCH=2.0,FIXED_PULL=0.1,CORR_STR=1.0,CORR_SMOOTH=0.0,PITCH_SHIFT=1.0,LFO_DEPTH=0.1,LFO_RATE=1.0,LFO_SHAPE=0.0,LFO_SYMM=0.0,FORM_WARP=0.0,MIX=1.0,KEY="c")
        for i in range(input.getBuffer(chanl=0)):
            self.Signal1[i]=input.getBuffer(chanl=0)[i]
        for i in range(input.getBuffer(chanl=1)):
            self.Signal2[i]=input.getBuffer(chanl=1)[i]
        self._FS=input.getSamplingRate()
        self._CHUNK=CHUNK
        self._SCALE_ROTATE=SCALE_ROTATE
        self._LFO_QUANT=LFO_QUANT
        self._CONCERT_A=CONCERT_A
        self._FIXED_PITCH=FIXED_PITCH
        self._FIXED_PULL=FIXED_PULL
        self._CORR_STR=CORR_STR
        self._CORR_SMOOTH=CORR_SMOOTH
        self._PITCH_SHIFT=PITCH_SHIFT
        self._LFO_DEPTH=LFO_DEPTH
        self._LFO_RATE=LFO_RATE
        self._LFO_SHAPE=LFO_SHAPE
        self._LFO_SYMM=LFO_SYMM
        self._FORM_WARP=FORM_WARP
        self._MIX=MIX
        self._KEY=KEY
    def setKey(self,key):
        self.KEY=key
    def setFS(self,fs):
        self._FS=fs
    def setChunk(self,chunk):
        self._CHUNK=chunk
    @property
    def key(self):
        self._key
    @key.setter
    def key(self,x):
        self.setKey(x)
    def out(self):
        a=[]
        b=[]
        for i in range(self.Signal1):
            a[i]=self.Signal1[i]
            b[i]=self.Signal2[i]
        l=AutoTune.Tuner(a,self.FS,self.CHUNK,self.SCALE_ROTATE,self.LFO_QUANT,self.CONCERT_A,self.FIXED_PITCH,self.FIXED_PULL,self.CORR_STR,self.CORR_SMOOTH,self.PITCH_SHIFT,self.LFO_DEPTH,self.LFO_RATE,self.LFO_SHAPE,self.LFO_SYMM,self.FORM_WARP,self.MIX,self.KEY)
        r=AutoTune.Tuner(b,self.FS,self.CHUNK,self.SCALE_ROTATE,self.LFO_QUANT,self.CONCERT_A,self.FIXED_PITCH,self.FIXED_PULL,self.CORR_STR,self.CORR_SMOOTH,self.PITCH_SHIFT,self.LFO_DEPTH,self.LFO_RATE,self.LFO_SHAPE,self.LFO_SYMM,self.FORM_WARP,self.MIX,self.KEY)
        pyo.Osc(table=l).out(chnl=0)
        pyo.Osc(table=r).out(chnl=1)

import pyo
s=pyo.Server(nchnls=2).boot()
s.start()
left_in=pyo.Input([0],mul=0.5)
right_in=pyo.Input([1],mul=0.5)
a=left_in+right_in
b=pyo.Chorus(a)
c=pyo.ButLP(b,freq=75)
d1=pyo.ButHP(c,175)
d2=pyo.ButHP(d1,175)
d3=pyo.ButHP(d2,175)
d4=pyo.ButHP(d3,75)
d5=pyo.ButHP(d4,75)
e=pyo.ButBR(d5,7000)
left_only=left_in*(0.0625)
right_only=right_in*(0.0625)
left_out=left_only+e
right_out=right_only+e
left_out_normalized=pyo.Tanh(left_out)
right_out_normalized=pyo.Tanh(right_out)
left_out_normalized.out([0])
right_out_normalized.out([1])
Follower=pyo.PeakAmp((left_out_normalized+right_out_normalized)/2.0)
print(Follower.get())
