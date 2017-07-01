import PIL.Image
from PIL import ImageFilter
import six
from array import array
import io
import StringIO
from Tkinter import Tk,Frame,Canvas,Label
import PIL.ImageTk


in_file='squwbs1.gif'
out_file='myImage.byte'
t=Tk()
t.title("Transparency")
canvas=Canvas(t,bg='black',width=200,height=200)
img=PIL.Image.open(in_file)

photo=PIL.ImageTk.PhotoImage(img)
canvas.create_image(50,50,image=photo,anchor='nw')
canvas.pack()
with open(in_file, 'rb') as file:
    a=bytearray(file.read())

with open(out_file,'w') as file:
    file.write(a)

t.mainloop()
