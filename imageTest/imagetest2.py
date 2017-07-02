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
img=PIL.Image.open(in_file)
photo=PIL.ImageTk.PhotoImage(img)
canvas=Canvas(t,bg='black',width=200,height=200)
canvas.create_image(100,100,image=photo)
canvas.pack()
label=Label(t,image=photo)
label.image=photo
#label.text="test"
label.pack()

with open(in_file, 'rb') as file:
    a=bytearray(file.read())

with open(out_file,'w') as file:
    file.write(a)

t.mainloop()
