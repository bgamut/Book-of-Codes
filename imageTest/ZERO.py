from time import clock,sleep
import wx
from numpy import *
import sys
from wx.lib.floatcanvas import FloatCanvas
from random import randint, random,uniform
import math

points=[(0,0),(0,0),(0,0),(0,0),(0,0)]
class tick():
    def __init__(self):
        self.number=0
    def update(self):
        self.number+=1
class DrawFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.tick=0
        self.points=[]
        super(DrawFrame, self).__init__(parent,*args, **kwargs)
        
        ## Set up the MenuBar

        MenuBar = wx.MenuBar()
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_TIMER,self.OnTimer)
        self.Canvas = FloatCanvas.FloatCanvas(self,-1,(500,500),
                                          Debug = False,
                                          BackgroundColor = "BLACK")
        self.Canvas.NumBetweenBlits = 1000
        self.OnTimer(None)
        self.timer=wx.Timer(self,-1)
        self.timer.Start(2)
        self.points=[]
        self.Show(True)
        self.DrawTest(None)




    
    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()
    
    def Clear(self,event = None):
        #self.Canvas.ClearAll()
        self.Canvas.InitAll()
        self.Canvas.Draw()
    
    def OnQuit(self,event):
        self.Close(True)

    def OnTimer(self,event):
        self.Clear()
        self.DrawTest()
        #self.Refresh()
    
    def OnCloseWindow(self, event):
        self.Destroy()
    def tick(self):
        self.ticknum=self.ticknum+1
    def DrawTest(self,event = None):
        a=uniform(0,6.29)
        b=uniform(0,100.0)
        point=(math.cos(a)*b,math.sin(a)*b)
        self.tick += 1
        if len(self.points)>4:
            if(self.tick%5==0):
                self.points.pop(0)
                self.Canvas.AddSpline((self.points[0],self.points[1],self.points[2],self.points[3],self.points[4]), LineWidth=4,LineColor="WHITE")
        self.points.append(point)
        print(self.points)
        c=self.points
        Canvas = self.Canvas
        #self.Canvas.AddPointSet(c,Color = "WHITE", Diameter = 4, InForeground = True)
        self.Canvas.Draw(Force=True)



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
