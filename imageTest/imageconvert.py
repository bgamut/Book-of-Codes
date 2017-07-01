import base64
import cStringIO
import PIL.Image
#import PIL.ImageTk
import re
from io import BytesIO

in_file='squwbs1.gif'
out_file_bin='image.data'
out_file_64='image64.data'

with open(in_file, 'rb') as file:
    #a=bytearray(file.read())
    a=file.read()
    b=base64.b64encode(a)
    #print("base64 = "+b)
with open(out_file_bin,'w') as file:
    file.write("image_data="+repr(a))
with open(out_file_64,'w') as file:
    file.write("image_data="+repr(b))
#read from binary(?)
#img=PIL.Image.open(cStringIO.StringIO(a))

#read from base64
img=PIL.Image.open(BytesIO(base64.b64decode(b)))
img.show()

#use from image.data import image_data to use image
