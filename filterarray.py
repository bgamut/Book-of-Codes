import math


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
from scipy.io.wavfile import write
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
        self.mid_averages=[]
        self.mid_standard_deviations=[]
        self.side_averages=[]
        self.side_standard_deviations=[]
        self.basepath=''
        """
        self.timer = wx.Timer(self, 1)
        self.count = 0
        self.gauge = wx.Gauge(panel, -1)
        """
        for i in range(len(self.barkscale)+1):
            self.mid_averages.append(0)
            self.side_averages.append(0)
            self.mid_standard_deviations.append(0)
            self.side_standard_deviations.append(0)
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mastering")
        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory= os.getcwd()
        openFileDlgBtnOne = wx.Button(panel, label = "OPEN Reference")
        openFileDlgBtnOne.Bind(wx.EVT_BUTTON,self.onOpenReference)
        openFileDlgBtnTwo = wx.Button(panel, label = "OPEN Original")
        saveLocationBtn = wx.Button(panel, label='Choose Save Directory')
        saveLocationBtn.Bind(wx.EVT_BUTTON,self.saveLocation)
        openFileDlgBtnTwo.Bind(wx.EVT_BUTTON,self.onOpenOriginal)
        runFileDlgBtn = wx.Button(panel, label = 'Run Mastering')
        runFileDlgBtn.Bind(wx.EVT_BUTTON,self.mastering)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(openFileDlgBtnOne, 0,wx.ALL|wx.CENTER,5)
        sizer.Add(openFileDlgBtnTwo, 0,wx.ALL|wx.CENTER,5)
        sizer.Add(saveLocationBtn, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(runFileDlgBtn, 0,wx.ALL|wx.CENTER,5)
        
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
        av=[]
        st=[]
        print('analyzing')
        for i in range(len(self.barkscale)+1):
            av.append(0)
            st.append(0)
        print("average analysis")
        tempfiltered = LP48(buffer,51,sr)
        for i in range(len(buffer)):
            print("0 / "+str(len(self.barkscale))+" - "+str(i)+" / "+str(len(buffer)))
            
            
            av[0]+=abs(tempfiltered[i]/len(buffer))
        
        tempfiltered = HP48(buffer,19500,sr)   
        for i in range(len(buffer)):
            print("1 / "+str(len(self.barkscale))+" - "+str(i)+" / "+str(len(buffer)))
            
            av[-1]+=abs(tempfiltered[i]/len(buffer))
        for i in range(len(self.barkscale)-1):
            tempfiltered=LP48(HP48(buffer,barkscale[i],sr),barkscale[i]+1,sr)
            for j in range(len(buffer)):
                print(str(i+2)+" / "+str(len(self.barkscale))+" - "+str(j)+" / "+str(len(buffer)))
                av[i+1]+=abs(tempfiltered[j])/len(buffer)
        print("standard deviation analysis")
        tempfiltered = LP48(buffer,51,sr)
        for i in range(len(buffer)):
            st[0]+=abs(abs(tempfiltered[i])-av[0])/len(buffer)
            print("0 / "+str(len(self.barkscale))+" - "+str(i)+" / "+str(len(buffer)))
        tempfiltered = HP48(buffer,19500,sr)
        for i in range(len(buffer)):
            print("1 / "+str(len(self.barkscale))+" - "+str(i)+" / "+str(len(buffer)))
            st[-1]+=(abs(abs(tempfiltered[i])-av[-1])/len(buffer))
        for i in range(len(self.barkscale)-1):
            tempfiltered = LP48(HP48(buffer,barkscale[i],sr),barkscale[i]+1,sr)
            for j in range(len(buffer)):
                print(str(i+2)+" / "+str(len(self.barkscale))+" - "+str(j)+" / "+str(len(buffer)))
                st[i+1]+=abs(abs(tempfiltered[j])-av[i+1])/len(buffer)
        obj.append(av)
        obj.append(st)
        return obj
    def produceBuffer(self,originalaverage,referenceaverage,standardRatio,originalbuffer,originalsr):
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
        temp = []
        print("Generating Master Buffer")
        for i in range(len(originalbuffer)):
            print("0 / "+str(len(barkscale))+str(i)+"/"+str(len(originalbuffer))) 
            new_buffer=LP48(originalbuffer,barkscale[0],originalsr)[i]
            if (originalbuffer[i]>0):
                temp.append((new_buffer[i]-originalaverage[0])*standardRatio[0]+referenceaverage[0])
            elif (originalbuffer[i]<0):
                temp.append((new_buffer[i]+originalaverage[0])*standardRatio[0]-referenceaverage[0])
            elif (originalbuffer[i]==0):
                temp.append(0)
        for i in range(len(self.barkscale)-1):
            
            new_buffer = LP48(HP48(originalbuffer,barkscale[i],originalsr),barkscale[i+1],originalsr)
            for j in range(len(originalbuffer)):
                print(str(i+1)+" / "+str(len(barkscale))+str(j)+"/"+str(len(originalbuffer))) 
                if (new_buffer[i]>0):
                    temp.append((new_buffer[i]-originalaverage[i+1])*standardRatio[i+1]+referenceaverage[i+1])
                elif (new_buffer[i]<0):
                    temp.append((new_buffer[i]+originalaverage[i+1])*standardRatio[i+1]-referenceaverage[i+1])
                elif (new_buffer[i]==0):
                    temp.append(0)
        for i in range(len(originalbuffer)):
            print(str(len(barkscale))+" / "+str(len(barkscale))+str(i)+"/"+str(len(originalbuffer))) 
            new_buffer=HP48(originalbuffer,barkscale[0],originalsr)[i]
            if (new_buffer[i]>0):
                temp[i]+=((new_buffer[i]-originalaverage[-1])*standardRatio[-1]+referenceaverage[-1])
            elif (new_buffer[i]<0):
                temp+=((new_buffer[i]+originalaverage[-1])*standardRatio[-1]-referenceaverage[-1])
            elif (new_buffer[i]==0):
                temp+=(0)  
        return temp

    def saveLocation(self, event):
        dlg = wx.DirDialog(
            self, "Choose the directory that the mastered files will be saved.",
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print ("You chose the following path")
            
    
            self.basePath=path
            
            print(self.basePath)


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
                a=read(self.originalpath[i])
                print(a)
                """        
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

    def mastering(self,event):
        for file in self.referencepath:
            a=read(file)
            left = []
            right = []
            mid = []
            side = []
            try:
                divideby = (np.iinfo(a[1]).min)*(-1)
            except:
                divideby = 1
            if (type(a[1]) is list):
                for i in range(len(a[1])):
                    left.append(a[1][i][0]/divideby)
                    right.append(a[1][i][1]/divideby)
                for i in range(len(left)):
                    mid.append((left[i]+right[i])/2.0)
                    side.append(left[i]-mid[i])
            elif (type(a[1]) is not int):
                for i in range(len(a[1])):
                    mid.append(a[1][i])
                    side.append(0)
            print("Reference Analysis Sequence 1/2")
            temp_mid=self.analysebuffer(mid, a[0])
            print("Reference Analysis Sequence 2/2")
            temp_side=self.analysebuffer(side, a[0])
            for i in range(len(self.referencepath)):
                self.mid_averages+=temp_mid[0][i]/len(self.referancepath)
                self.mid_standard_deviations+=temp_mid[1][i]/len(self.referancepath)
                self.side_averages+=temp_side[0][i]/len(self.referancepath)
                self.side_standard_deviations+=temp_side[1][i]/len(self.referancepath)
        for file in self.originalpath:
            a=read(file)
            left = []
            right = []
            mid = []
            side = []
            mid_average_ratio=[]
            mid_standard_ratio=[]
            side_average_ratio=[]
            side_standard_ratio=[]
            obj=[]
            if (type(a[1]) is list):
                for i in range(len(a[1])):
                    left.append(a[1][i][0])
                    right.append(a[1][i][1])
                for i in range(len(left)):
                    mid.append((left[i]+right[i])/2.0)
                    side.append(left[i]-mid[i])
            elif (type(a[1]) is not int):
                for i in range(len(a[1])):
                    mid.append(a[1][i])
                    side.append(0)
            print("Original Track Analysis Sequence 1/2")
            temp_mid=self.analysebuffer(mid, a[0])
            print("Original Track Analysis Sequence 2/2")
            temp_side=self.analysebuffer(side, a[0])
            
            mid_averages=temp_mid[0]
            mid_standard_deviations=temp_mid[1]
            side_averages=temp_side[0]
            side_standard_deviations=temp_side[1]
            for i in range(len(self.mid_averages)):
                mid_average_ratio.append(self.mid_averages[i]/mid_averages[i])
                mid_standard_ratio.append(self.mid_standard_deviations[i]/mid_standard_deviations[i])
                side_average_ratio.append(self.side_averages[i]/side_averages[i])
                side_standard_ratio.append(self.side_standard_deviation[i]/side_standard_deviations[i])
            obj.append(mid_average_ratio)
            obj.append(mid_standard_ratio)
            obj.append(side_average_ratio)
            obj.append(side_standard_ratio)
            mid=self.producebuffer(mid_averages,self.mid_averages,mid_standard_ratio,temp_mid,a[0])
            side=self.producebuffer(side_averages,self.side_averages,side_standard_ratio,temp_side,a[0])
            master = np.zeros((len(mid),2),'int16')
            for i in range(len(mid)):
                master[i][0]=(mid[i]+side[i])*np.iinfo('int16').max
                master[i][1]=(mid[i]-side[i])*np.iinfo('int16').max
            master = np.zeros((len(mid),2),'int16')
            #need to iterate through file names and foldername for the code below
            filename=os.path.basename(file)
            newfilename = os.path.join(self.basepath,+filename)
            write(newfilename,a[0],master)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
