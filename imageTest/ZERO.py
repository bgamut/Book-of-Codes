from time import clock,sleep
import wx
from numpy import *
import sys
from wx.lib.floatcanvas import FloatCanvas
from random import randint, random,uniform
from math import cos,sin,sqrt,pi
from time import sleep


class tick():
    def __init__(self):
        self.number=0
    def update(self):
        self.number+=1
class DrawFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.tick=0
        self.BPM=90.0
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
                                          BackgroundColor = "WHITE")
        self.Canvas.NumBetweenBlits = 1000
        self.OnTimer(None)
        self.timer=wx.Timer(self,-1)
        self.timer.Start(4)
        self.points=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        self.Show(True)
        self.DrawTest(None)




    
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
        self.Destroy()
    def tick(self):
        self.ticknum=self.ticknum+1
    def DrawTest(self,event = None):
        w, h = self.GetClientSize()
        a=uniform(0,2*pi)
        #b=uniform(0,100.0)
        #b=sqrt(w*w+h*h)/3
        b=min(w,h)/2
        c=uniform(0,min(w,h)/2)
        point=(cos(a)*c,sin(a)*c)
        self.tick += 1
        self.points.append(point)
        self.points.pop(0)

        if(self.tick%8==0):
            self.Canvas.AddCircle((0,0), b*(1.0+sqrt(5))/4.0, LineWidth = b/2.0,LineColor = "BLACK",FillColor = "WHITE")

            self.Canvas.AddSpline((self.pppoints[2],self.pppoints[3],self.pppoints[4],self.pppoints[5],self.pppoints[6],self.pppoints[7],self.pppoints[8],self.pppoints[9],self.ppoints[1],self.ppoints[2],self.ppoints[3]), LineWidth=5,LineColor="BLACK")
            self.Canvas.AddSpline((self.pppoints[2],self.pppoints[3],self.pppoints[4],self.pppoints[5],self.pppoints[6],self.pppoints[7],self.pppoints[8],self.pppoints[9],self.ppoints[1],self.ppoints[2],self.ppoints[3]), LineWidth=5,LineColor="#AAAAAA")
            self.Canvas.AddSpline((self.ppoints[2],self.ppoints[3],self.ppoints[4],self.ppoints[5],self.ppoints[6],self.ppoints[7],self.ppoints[8],self.ppoints[9],self.points[0],self.points[1]), LineWidth=8,LineColor="BLACK")
            self.Canvas.AddSpline((self.ppoints[2],self.ppoints[3],self.ppoints[4],self.ppoints[5],self.ppoints[6],self.ppoints[7],self.ppoints[8],self.ppoints[9],self.points[0],self.points[1]), LineWidth=7,LineColor="#FAFAFA")
            self.Canvas.AddSpline((self.points[0],self.points[1],self.points[2],self.points[3],self.points[4],self.points[5],self.points[6],self.points[7],self.points[8],self.points[9]), LineWidth=8,LineColor="BLACK")
            self.Canvas.AddSpline((self.points[0],self.points[1],self.points[2],self.points[3],self.points[4],self.points[5],self.points[6],self.points[7],self.points[8],self.points[9]), LineWidth=6,LineColor="WHITE")
            self.Canvas.Draw(Force=True)
            for i in range(len(self.points)):
                self.ppoints[i]=self.points[i]
                self.pppoints[i]=self.ppoints[i]
            #self.Canvas.AddPointSet(self.points,Color = "WHITE", Diameter = 4)

        #print(self.points)


        wx.GetApp().Yield(onlyIfNeeded=True)



class DemoApp(wx.App):
    def OnInit(self):
        frame = DrawFrame(None,
                          title="ZERO",
                          size=(200,200),
                          )
        self.SetTopWindow(frame)

        return True

if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()
