import wx
from wx import glcanvas
from OpenGL.GL import *

class GLFrame(wx.Frame):
    def __init__(self, parent,id,title,pos=wx.DefaultPosition,size=wx.DefaultSize,style=wx.DEFAULT_FRAME_STYLE,name='frame'):
        style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE
        super(GLFrame, self).__init__(parent,id,title,pos,size,style,name)
        self.GLinitialized =False
        attribList = (glcanvas.WX_GL_RGBA,glcanvas.WX_GL_DOUBLEBUFFER,glcanvas.WX_GL_DEPTH_SIZE,24)
        self.canvas = glcanvas.GLCanvas(self,attribList=attribList)
        self.canvas.Bind(wx.EVT_ERASE_BACKGROUND,self.processEraseBackgroundEvent)
        self.canvas.Bind(wx.EVT_SIZE,self.processSizeEvent)
        self.canvas.Bind(wx.EVT_PAINT, self.processPaintEvent)
#
        self.context=glcanvas.GLContext(self.canvas)
#
    def GetGLExtents(self):
        return self.canvas.GetClientSize()
    def SwapBuffers(self):
        self.canvas.SwapBuffers()
    def processEraseBackgroundEvent(self,event):
        pass
    def processSizeEvent(self,event):
        #if self.canvas.GetContext():
        if self.context:
            self.Show()
            #added self.context
            self.canvas.SetCurrent(self.context)
            #
            size=self.GetGLExtents()
            self.OnReshape(size.width,size.height)
            self.canvas.Refresh(False)
            event.Skip()
    def processPaintEvent(self,event):
        #
        self.canvas.SetCurrent(self.context)
        #
        if not self.GLinitialized:
            self.OnInitGL()
            self.GLinitialized = True
            self.OnDraw()
            event.Skip()
    def OnInitGL(self):
        glClearColor(1,1,1,1)
    def OnReshape(self,width,height):
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5,0.5,-0.5,0.5,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def OnDraw(self, *args, **kwargs):
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_TRIANGLES)
        glColor(0,0,0)
        glVertex(-0.25,-0.25)
        glVertex(0.25,0.25)
        glVertex(0,0.25)
        glEnd()
        self.SwapBuffers()
app = wx.App()
frame = GLFrame(None, -1, 'GL Window')
frame.Show()

app.MainLoop()
