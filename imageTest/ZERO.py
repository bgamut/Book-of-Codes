from time import clock,sleep
import wx
#from numpy import *
import sys
from wx.lib.floatcanvas import FloatCanvas
from random import randint


class DrawFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        
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
        self.timer.Start(33)
                         
        self.Show(True)
                         
        self.DrawTest(None)
        return None
    
    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()
    
    def Clear(self,event = None):
        self.Canvas.ClearAll()
        self.Canvas.Draw()
    
    def OnQuit(self,event):
        self.Close(True)

    def OnTimer(self,event):
        self.Clear()
        self.DrawTest()
    
    def OnCloseWindow(self, event):
        self.Destroy()
    
    def DrawTest(self,event = None):
        a=randint(-100,100)
        b=randint(-100,100)
        point=(a,b)
        #print(point)
        Canvas = self.Canvas
        self.Canvas.AddPointSet(point,Color = "WHITE", Diameter = 4, InForeground = True)
        self.Canvas.Draw()

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
