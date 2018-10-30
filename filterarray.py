import math

def filter(buffer,mode="HP48",sr=44100,freq=175,resonance=0):
    new_buffer=[]
    for i in range(len(buffer)):
        new_buffer.append(0)
    cutoff=2*math.sin(math.pi*(freq/sr))
    feedbackAmount = resonance + resonance/(1.0-cutoff)
    buf0 = 0
    buf1 = 0
    buf2 = 0
    buf3 = 0
    buf4 = 0
    buf5 = 0
    buf6 = 0
    buf7 = 0
    buf8 = 0
    buf9 = 0
    buf10 = 0
    buf11 = 0
    buf12 = 0
    buf13 = 0
    buf14 = 0
    buf15 = 0
    if (mode == "HP12"):
        for i in range(len(buffer)):
            """
            buf0 = buf0+cutoff*(buffer[i]*buf0)
            """
            buf0 += cutoff * (buffer[i] - buf0)
            buf1 += cutoff * (buf0 - buf1)
            new_buffer[i]=buffer[i]-buf1
        
    elif (mode =="LP12"):
        for i in range(len(buffer)):
            
            buf0 = buf0+cutoff*(buffer[i]*buf0)
            buf1 = buf1+cutoff*(buf0-buf1)
            new_buffer[i]=buf1
    elif (mode == "HP48"):
        print('in HP48')
        for i in range(len(buffer)):
            buf0 += cutoff * (buffer[i] - buf0)
            buf1 += cutoff * (buf0 - buf1)
            buf2 += cutoff * (buf1 - buf2)
            buf3 += cutoff * (buf2 - buf3)
            buf4 += cutoff * (buf3 - buf4)
            buf5 += cutoff * (buf4 - buf5)
            buf6 += cutoff * (buf5 - buf6)
            buf7 += cutoff * (buf6 - buf7)
            new_buffer[i]=buffer[i] - buf7
    elif(mode=="LP48"):
        for i in range(len(buffer)):
            buf0 += cutoff * (buffer[i] - buf0)
            buf1 += cutoff * (buf0 - buf1)
            buf2 += cutoff * (buf1 - buf2)
            buf3 += cutoff * (buf2 - buf3)
            buf4 += cutoff * (buf3 - buf4)
            buf5 += cutoff * (buf4 - buf5)
            buf6 += cutoff * (buf5 - buf6)
            buf7 += cutoff * (buf6 - buf7)
            new_buffer[i]=buf7
    elif(mode=="LP96"):
        for i in range(len(buffer)):
            buf0 += cutoff * (buffer[i] - buf0)
            buf1 += cutoff * (buf0 - buf1)
            buf2 += cutoff * (buf1 - buf2)
            buf3 += cutoff * (buf2 - buf3)
            buf4 += cutoff * (buf3 - buf4)
            buf5 += cutoff * (buf4 - buf5)
            buf6 += cutoff * (buf5 - buf6)
            buf7 += cutoff * (buf6 - buf7)
            buf8 += cutoff * (buf7 - buf8)
            buf9 += cutoff * (buf8 - buf9)
            buf10 += cutoff * (buf9 - buf10)
            buf11 += cutoff * (buf10 - buf11)
            buf12 += cutoff * (buf11 - buf12)
            buf13 += cutoff * (buf12 - buf13)
            buf14 += cutoff * (buf13 - buf14)
            buf15 += cutoff * (buf14 - buf15)
           
            new_buffer[i]=buf15
    return new_buffer

def read_wav_file(input_file_path,output_file_path):
    from scipy.io.wavfile import read
    a=read(input_file_path)
    import json
    import numpy as np 
    b=[]
    for i in range(len(a[1])):
        b.append(a[1][i][0])

    c=np.asarray(b)
    d=c.tolist()
    e=json.dumps(d)

    file = open(output_file_path,'w')
    file.write(e)
    file.close()




import os
import wx
import wx.lib.agw.multidirdialog as MDD
from scipy.io.wavfile import read
import numpy as np 
import math
wildcard = "Python source (*.py) |*.py|" \
            "All files (*.*)|*.*"
originalpath=[]
referencepath=[]
barkscale = [0,51,127,200,270,370,440,530,640,770,950,1200,1550,19500]
class MyForm(wx.Frame):
    def __init__(self):
        self.barkscale = [51,127,200,270,370,440,530,640,770,950,1200,1550,19500]
        self.referencepath=[]
        self.originalpath=[]
        self.averages=[]
        self.standard_deviations=[]
        for i in range(len(self.barkscale)+1):
            self.averages.append(0)
            self.standard_deviations.append(0)
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mastering")
        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory= os.getcwd()
        openFileDlgBtnOne = wx.Button(panel, label = "Show OPEN Reference")
        openFileDlgBtnOne.Bind(wx.EVT_BUTTON,self.onOpenReference)
        openFileDlgBtnTwo = wx.Button(panel, label = "Show OPEN Original")
        openFileDlgBtnTwo.Bind(wx.EVT_BUTTON,self.onOpenOriginal)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(openFileDlgBtnOne, 0,wx.ALL|wx.CENTER,5)
        sizer.Add(openFileDlgBtnTwo, 0,wx.ALL|wx.CENTER,5)
        panel.SetSizer(sizer)
    def analysebuffer(self,buffer,sr):
        def LP48(buffer,freq,sr):
            buf0 = 0
            buf1 = 0
            buf2 = 0
            buf3 = 0
            buf4 = 0
            buf5 = 0
            buf6 = 0
            buf7 = 0
            cutoff=2*math.sin(math.pi*(freq/sr))
            new_buffer=[]
            for i in range(len(buffer)):
                buf0 += cutoff * (buffer[i] - buf0)
                buf1 += cutoff * (buf0 - buf1)
                buf2 += cutoff * (buf1 - buf2)
                buf3 += cutoff * (buf2 - buf3)
                buf4 += cutoff * (buf3 - buf4)
                buf5 += cutoff * (buf4 - buf5)
                buf6 += cutoff * (buf5 - buf6)
                buf7 += cutoff * (buf6 - buf7)
                new_buffer.append(buf7)
            return new_buffer
        def HP48(buffer,freq,sr):
            buf0 = 0
            buf1 = 0
            buf2 = 0
            buf3 = 0
            buf4 = 0
            buf5 = 0
            buf6 = 0
            buf7 = 0
            cutoff=2*math.sin(math.pi*(freq/sr))
            new_buffer=[]
            for i in range(len(buffer)):
                buf0 += cutoff * (buffer[i] - buf0)
                buf1 += cutoff * (buf0 - buf1)
                buf2 += cutoff * (buf1 - buf2)
                buf3 += cutoff * (buf2 - buf3)
                buf4 += cutoff * (buf3 - buf4)
                buf5 += cutoff * (buf4 - buf5)
                buf6 += cutoff * (buf5 - buf6)
                buf7 += cutoff * (buf6 - buf7)
                new_buffer.append(buffer[i] - buf7)
            return new_buffer
        obj=[]
        
        for i in range(len(buffer)):
            self.averages[0]+=abs(LP48(buffer,51,sr)[i])/len(buffer)
            self.averages[-1]+=abs((HP48(buffer,19500,sr)[i])/len(buffer))
        for i in range(len(self.barkscale-1)):
            for j in range(len(buffer)):
                self.averages[i+1]+=abs(LP48(HP48(buffer,barkscale[i],sr),barkscale[i]+1,sr)[j])/len(buffer)
        for i in range(len(buffer)):
            self.standard_deviations[0]+=(abs(LP48(buffer,51,sr)[i])-self.averages[0])/len(buffer)
            self.standard_deviations[-1]+=(abs((HP48(buffer,19500,sr)[i])-self.averages[-1])/len(buffer))
        for i in range(len(self.barkscale-1)):
            for j in range(len(buffer)):
                self.standard_deviations[i+1]+=abs(LP48(HP48(buffer,barkscale[i],sr),barkscale[i]+1,sr)[j]-self.averages[i+1])/len(buffer)
        obj.append(self.averages)
        obj.append(self.standard_deviations)
        return obj




    def onOpenReference(self, event):
        dlg = wx.FileDialog(
            self, message = "Choose a reference track",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard='*.wav',
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print ("You chose the following files")
            for path in paths:
                
                self.originalpath.append(path)
            for i in range(len(self.originalpath)):
                print (self.originalpath[i])
                """
                a=read(path)        
                b=[]
                for i in range(len(a[1])):
                    b.append(a[1][i][0])
                c=np.asarray(b)
                d=c.tolist()
                print(d)
                """
                
            
    def onOpenOriginal(self, event):
        dlg = wx.FileDialog(
            self, message = "Choose your original track",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard='*.wav',
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print ("You chose the following files")
            for path in paths:
                self.referencepath.append(path)
            for i in range(len(self.referencepath)):
                print (self.referencepath[i])

    def 
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
