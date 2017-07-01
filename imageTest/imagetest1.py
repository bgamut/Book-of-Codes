import PIL.Image
from PIL import ImageFilter
from Tkinter import *
import six
from array import array
import io
import StringIO

in_file='squwbs1.png'
out_file='myImage.byte'
with open(in_file, 'rb') as file:
    a=bytearray(file.read())

with open(out_file,'w') as file:
    file.write(a)

image1 = PIL.Image.open(StringIO.StringIO(a))
image2=image1.filter(ImageFilter.GaussianBlur(5))
image2.show()
