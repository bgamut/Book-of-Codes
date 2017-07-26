from time import clock,sleep
import wx
from numpy import *
import numpy as np
import sys
import scipy.fftpack
from wx.lib.floatcanvas import FloatCanvas
from random import randint, random,uniform
from math import cos,sin,sqrt,pi,fabs
from time import sleep
import pyo
import threading
import AutoTune
def zerolist(n):
    return [0.0]*n
class Autotune(pyo.PyoObject):
    def __init__(self, input, mul=1,add=0, FS=44100.0,CHUNK=256,SCALE_ROTATE=0,LFO_QUANT=0,CONCERT_A=440.0,FIXED_PITCH=2.0,FIXED_PULL=0.1,CORR_STR=1.0,CORR_SMOOTH=0.0,PITCH_SHIFT=1.0,LFO_DEPTH=0.1,LFO_RATE=1.0,LFO_SHAPE=0.0,LFO_SYMM=0.0,FORM_WARP=0.0,MIX=1.0,KEY="c"):
        self.Signal=[]
        pyo.PyoObject.__init__(self,mul,add)
        for i in range(len(input.get(all=True))-1):
            self.Signal[i]=input.get(all=True)[i]
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
        for i in range(self.Signal):
            a[i]=self.Signal[i]
        l=AutoTune.Tuner(a,self.FS,self.CHUNK,self.SCALE_ROTATE,self.LFO_QUANT,self.CONCERT_A,self.FIXED_PITCH,self.FIXED_PULL,self.CORR_STR,self.CORR_SMOOTH,self.PITCH_SHIFT,self.LFO_DEPTH,self.LFO_RATE,self.LFO_SHAPE,self.LFO_SYMM,self.FORM_WARP,self.MIX,self.KEY)
        return pyo.Osc(table=l).out(self)
    def play(self):
        a=[]
        for i in range(self.Signal1):
            a[i]=self.Signal[i]
        l=AutoTune.Tuner(a,self.FS,self.CHUNK,self.SCALE_ROTATE,self.LFO_QUANT,self.CONCERT_A,self.FIXED_PITCH,self.FIXED_PULL,self.CORR_STR,self.CORR_SMOOTH,self.PITCH_SHIFT,self.LFO_DEPTH,self.LFO_RATE,self.LFO_SHAPE,self.LFO_SYMM,self.FORM_WARP,self.MIX,self.KEY)
        return pyo.Osc(table=l).play(self)
    def stop(self):
        a=[]
        for i in range(self.Signal1):
            a[i]=self.Signal[i]
        l=AutoTune.Tuner(a,self.FS,self.CHUNK,self.SCALE_ROTATE,self.LFO_QUANT,self.CONCERT_A,self.FIXED_PITCH,self.FIXED_PULL,self.CORR_STR,self.CORR_SMOOTH,self.PITCH_SHIFT,self.LFO_DEPTH,self.LFO_RATE,self.LFO_SHAPE,self.LFO_SYMM,self.FORM_WARP,self.MIX,self.KEY)
        return pyo.Osc(table=l)

s=pyo.Server(nchnls=2).boot()
s.start()
left=pyo.Input([0],mul=0.5)
right=pyo.Input([1],mul=0.5)
left_in=pyo.Gate(left,risetime=0.015)
right_in=pyo.Gate(right,risetime=0.015)
la=left_in
lb=pyo.Chorus(la,bal=0.1)
lc=pyo.ButHP(lb,40)
ld1=pyo.ButHP(lc,40)
ld2=pyo.ButLP(ld1,2250)
ld3=pyo.ButLP(ld2,7000)
ld4=pyo.ButLP(ld3,7000)
ld5=pyo.ButLP(ld4,7000)
le=pyo.ButBR(ld5,3880)
lf=pyo.ButBR(le,7000)
ra=right_in
rb=pyo.Chorus(ra,bal=0.1)
rc=pyo.ButHP(rb,40)
rd1=pyo.ButHP(rc,40)
rd2=pyo.ButLP(rd1,2250)
rd3=pyo.ButLP(rd2,7000)
rd4=pyo.ButLP(rd3,7000)
rd5=pyo.ButLP(rd4,7000)
re=pyo.ButBR(rd5,3880)
rf=pyo.ButBR(re,7000)
mid=left_in+right_in
mid_low=pyo.ButLP(mid,freq=40,mul=2)
left_out=mid_low+lf
right_out=mid_low+rf
#left_tuned=Autotune(left_out)
#right_tuned=Autotune(right_out)
#left_tuned=left_out
#right_tuned=right_out
left_out_normalized=pyo.Tanh(left_out,mul=10.0)
right_out_normalized=pyo.Tanh(right_out,mul=10.0)
left_out_normalized.out([0])
right_out_normalized.out([1])
Follower_left=pyo.PeakAmp(left_out_normalized,mul=(1.0/12.0))
Follower_right=pyo.PeakAmp(right_out_normalized,mul=(1.0/12.0))


class tick():
    def __init__(self):
        self.number=0
    def update(self):
        self.number+=1
class DrawFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.tick=0
        self.BPM=90.0
        self.a=0
        self.b=0
        self.left=0
        self.right=0
        self.c1=0
        self.c2=0
        self.d=0
        self.real=zerolist(256)
        self.fft=zerolist(128)
        self.fftturnt=[]
        self.pppoints=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        self.ppoints=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        self.points=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        self.dots=[]

        super(DrawFrame, self).__init__(parent,*args, **kwargs)
        
        ## Set up the MenuBar

        MenuBar = wx.MenuBar()
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_TIMER,self.OnTimer)
        self.Canvas = FloatCanvas.FloatCanvas(self,-1,(200,200),
                                          Debug = False,
                                          BackgroundColor = "BLACK")
        self.Canvas.NumBetweenBlits = 1000
        self.OnTimer(None)
        self.timer=wx.Timer(self,-1)
        self.timer.Start(2)
        self.points=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        self.Show(True)
        self.DrawTest(None)




    def fftCalc(self,real):
        self.fft=np.sqrt(np.abs(np.fft.fft(real).real[:len(real)//2]))
    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()

    def OnQuit(self,event):
        self.Close(True)

    def OnTimer(self,event):
        self.Canvas.InitAll()
        self.DrawTest()
        #wx.GetApp().Yield(onlyIfNeeded=True)
        #self.Refresh()
    
    def OnCloseWindow(self, event):
        #s.stop()
        sleep(2.00)
        self.Destroy()
    def tick(self):
        self.ticknum=self.ticknum+1
    def DrawTest(self,event = None):
        w, h = self.GetClientSize()
        self.a=uniform(0,2*pi)
        #b=uniform(0,100.0)
        #b=sqrt(w*w+h*h)/3
        self.b=min(w,h)/2
        #self.c1=uniform(0,min(w,h)/2)
        self.left=left_out_normalized.get()*min(w,h)/4
        self.right=right_out_normalized.get()*min(w,h)/4
        self.d=sqrt(fabs(self.left*self.right))
        point=(self.a*(self.right/sqrt(2.0)-self.left/sqrt(2)),self.a*(self.right/sqrt(2.0)+self.left/sqrt(2)))
        #print(left_out_normalized.get())
        self.tick += 1
        self.points.append(point)
        self.points.pop(0)
        self.c1=(self.right+self.left)*self.a/2.0
        self.real.append(self.c1)
        self.real.pop(0)
        #t=threading.Thread(target=self.fftCalc(self.real))
        if(self.tick%4==0):
            #self.fftCalc(self.real)
            #for i in range(128):
                #self.Canvas.AddPolygon([(0,-h/2),(0,-h/2+(h/2)*self.fft[i]/100.0),((w/128.0)*i,-h/2+(h/2)*self.fft[i]/100.0),((w/128.0)*i,-h/2)],LineColor="white",FillColor="WHITE")
                #self.Canvas.AddPolygon([(0,-h/2),(0,-h/2+(h/2)*self.fft[i]/100.0),(-(w/128.0)*i,-h/2+(h/2)*self.fft[i]/100.0),(-(w/128.0)*i,-h/2)],LineColor="white",FillColor="WHITE")
            self.Canvas.AddCircle((0,0), self.b*(1.0+sqrt(5))/2.0+self.d/48.0, LineWidth = 2.0,LineColor = "BLACK",FillColor = "WHITE")
            self.Canvas.AddSpline((self.ppoints[2],self.ppoints[3],self.ppoints[4],self.ppoints[5],self.ppoints[6],self.ppoints[7],self.ppoints[8],self.ppoints[9],self.points[0],self.points[1]), LineWidth=8,LineColor="BLACK")
            self.Canvas.AddSpline((self.points[0],self.points[1],self.points[2],self.points[3],self.points[4],self.points[5],self.points[6],self.points[7],self.points[8],self.points[9]), LineWidth=8,LineColor="BLACK")
            self.Canvas.AddSpline((self.pppoints[2],self.pppoints[3],self.pppoints[4],self.pppoints[5],self.pppoints[6],self.pppoints[7],self.pppoints[8],self.pppoints[9],self.ppoints[1],self.ppoints[2],self.ppoints[3]), LineWidth=5,LineColor="#AAAAAA")
            self.Canvas.AddSpline((self.ppoints[2],self.ppoints[3],self.ppoints[4],self.ppoints[5],self.ppoints[6],self.ppoints[7],self.ppoints[8],self.ppoints[9],self.points[0],self.points[1]), LineWidth=7,LineColor="#FAFAFA")
            self.Canvas.AddCircle((0,0), (self.c1/96.0+self.b*(1.0+sqrt(5))/6.0), LineWidth = 2,LineColor = "BLACK",FillColor = "WHITE")
            self.Canvas.AddSpline((self.points[0],self.points[1],self.points[2],self.points[3],self.points[4],self.points[5],self.points[6],self.points[7],self.points[8],self.points[9]), LineWidth=6,LineColor="WHITE")
            self.tick=0

            self.Canvas.Draw(Force=True)
            for i in range(len(self.points)):
                self.ppoints[i]=self.points[i]
                self.pppoints[i]=self.ppoints[i]
            #self.Canvas.AddPointSet(self.points,Color = "WHITE", Diameter = 4)
            self.c2=self.c1





        #print(Follower.get())
        wx.GetApp().Yield(onlyIfNeeded=True)



class DemoApp(wx.App):
    def OnInit(self):
        frame = DrawFrame(None,
                          title="ONE",
                          size=(200,200),
                          )
        self.SetTopWindow(frame)

        return True

if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()
