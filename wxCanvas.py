
# coding: utf-8


from time import clock
import wx
from numpy import *
import sys
import six
from wx.lib.floatcanvas import NavCanvas
from wx.lib.floatcanvas import FloatCanvas


ID_DRAW_BUTTON = 100
ID_QUIT_BUTTON = 101
ID_CLEAR_BUTTON = 103
ID_ZOOM_IN_BUTTON = 104
ID_ZOOM_OUT_BUTTON = 105
ID_ZOOM_TO_FIT_BUTTON = 110
ID_MOVE_MODE_BUTTON = 111
ID_TEST_BUTTON = 112

ID_ABOUT_MENU = 200           
ID_EXIT_MENU  = 201   
ID_ZOOM_IN_MENU = 202  
ID_ZOOM_OUT_MENU = 203 
ID_ZOOM_TO_FIT_MENU = 204
ID_DRAWTEST_MENU = 205
ID_DRAWMAP_MENU = 206
ID_CLEAR_MENU = 207


ID_TEST = 500




class DrawFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        
        ## Set up the MenuBar
        
        MenuBar = wx.MenuBar()
        
        file_menu = wx.Menu()
        file_menu.Append(ID_EXIT_MENU, "E&xit","Terminate the program")
        wx.EVT_MENU(self, ID_EXIT_MENU,       self.OnQuit)
        MenuBar.Append(file_menu, "&File")
        
        draw_menu = wx.Menu()
        draw_menu.Append(ID_DRAWTEST_MENU, "&Draw Test","Run a test of drawing random components")
        wx.EVT_MENU(self, ID_DRAWTEST_MENU,self.DrawTest)
        draw_menu.Append(ID_DRAWMAP_MENU, "Draw &Movie","Run a test of drawing a map")
        wx.EVT_MENU(self, ID_DRAWMAP_MENU,self.RunMovie)
        draw_menu.Append(ID_CLEAR_MENU, "&Clear","Clear the Canvas")
        wx.EVT_MENU(self, ID_CLEAR_MENU,self.Clear)
        MenuBar.Append(draw_menu, "&Draw")
        
        
        view_menu = wx.Menu()
        view_menu.Append(ID_ZOOM_TO_FIT_MENU, "Zoom to &Fit","Zoom to fit the window")
        wx.EVT_MENU(self, ID_ZOOM_TO_FIT_MENU,self.ZoomToFit)
        MenuBar.Append(view_menu, "&View")
        
        help_menu = wx.Menu()
        help_menu.Append(ID_ABOUT_MENU, "&About",
                                "More information About this program")
        wx.EVT_MENU(self, ID_ABOUT_MENU,      self.OnAbout)
        MenuBar.Append(help_menu, "&Help")
        
        self.SetMenuBar(MenuBar)
                
        self.CreateStatusBar()
        self.SetStatusText("")
        
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        
        # Other event handlers:
        wx.EVT_RIGHT_DOWN(self, self.RightButtonEvent)
        
        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                  Debug = False,
                                  BackgroundColor = "WHITE").Canvas
        self.Canvas.NumBetweenBlits = 1000
        self.Show(True)
        
        self.DrawTest(None)
        return None
    def RightButtonEvent(self,event):
        print ("Right Button has been clicked in DrawFrame") 
        print ("coords are: %i, %i"%(event.GetX(),event.GetY()))
        event.Skip()
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                                                  "the use of the FloatCanvas\n",
                                                  "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()
        
    def Clear(self,event = None):
        self.Canvas.ClearAll()
        self.Canvas.Draw()
        
    def OnQuit(self,event):
        self.Close(True)
        
    def OnCloseWindow(self, event):
        self.Destroy()
        
    def DrawTest(self,event = None):
        import random
        import numpy.random as RandomArray
         
        Range = (-10,10)

        colors = ["AQUAMARINE", "BLACK", "BLUE", "BLUE VIOLET", "BROWN",
                  "CADET BLUE", "CORAL", "CORNFLOWER BLUE", "CYAN", "DARK GREY",
                  "DARK GREEN", "DARK OLIVE GREEN", "DARK ORCHID", "DARK SLATE BLUE",
                  "DARK SLATE GREY", "DARK TURQUOISE", "DIM GREY",
                  "FIREBRICK", "FOREST GREEN", "GOLD", "GOLDENROD", "GREY",
                  "GREEN", "GREEN YELLOW", "INDIAN RED", "KHAKI", "LIGHT BLUE",
                  "LIGHT GREY", "LIGHT STEEL BLUE", "LIME GREEN", "MAGENTA",
                  "MAROON", "MEDIUM AQUAMARINE", "MEDIUM BLUE", "MEDIUM FOREST GREEN",
                  "MEDIUM GOLDENROD", "MEDIUM ORCHID", "MEDIUM SEA GREEN",
                  "MEDIUM SLATE BLUE", "MEDIUM SPRING GREEN", "MEDIUM TURQUOISE",
                  "MEDIUM VIOLET RED", "MIDNIGHT BLUE", "NAVY", "ORANGE", "ORANGE RED",
                  "ORCHID", "PALE GREEN", "PINK", "PLUM", "PURPLE", "RED",
                  "SALMON", "SEA GREEN", "SIENNA", "SKY BLUE", "SLATE BLUE",
                  "SPRING GREEN", "STEEL BLUE", "TAN", "THISTLE", "TURQUOISE",
                  "VIOLET", "VIOLET RED", "WHEAT", "WHITE", "YELLOW", "YELLOW GREEN"]   
        Canvas = self.Canvas

        # Some Polygons in the background:
#        for i in range(500):
#            points = RandomArray.uniform(-100,100,(10,2))
        for i in range(500):
#        for i in range(1):
            points = RandomArray.uniform(-100,100,(10,2))
            lw = random.randint(1,6)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            self.Canvas.AddPolygon(points,
                                   LineWidth = lw,
                                   LineColor = colors[cl],
                                   FillColor = colors[cf],
                                   FillStyle = 'Solid',
                                   InForeground = False)
            
        ## Pointset
        print ("Adding Points to Foreground") 
        for i in range(1):
            points = RandomArray.uniform(-100,100,(1000,2))
            D = 2
            self.LEs = self.Canvas.AddPointSet(points, Color = "Black", Diameter = D, InForeground = True)
            
        self.Canvas.AddRectangle((-200,-200), (400,400))
        Canvas.ZoomToBB()
        
    def RunMovie(self,event = None):
        import numpy.random as RandomArray
        start = clock()
        #shift = RandomArray.randint(0,0,(2,))
        for i in range(100):
            points = self.LEs.Points
            shift = RandomArray.randint(-5,6,(2,))
            points += shift
            self.LEs.SetPoints(points)
            self.Canvas.Draw()
            wx.GetApp().Yield(True)
        print ("running the movie took %f seconds"%(clock() - start))


class DemoApp(wx.App):
    def OnInit(self):
        frame = DrawFrame(None,
                          title="Simple Drawing Window",
                          size=(700,700),
                        )
        self.SetTopWindow(frame)

        return True



if __name__ == "__main__":
    app=DemoApp(0)
    app.MainLoop()




