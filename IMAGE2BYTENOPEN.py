#converts an image to byte string and saves it to a file and then Image opens a bytearray
#vim open any file and the result is a bytearray.

from PIL import Image
import six
from array import array
import io

in_file='squwbs.png'
out_file='myImage.byte'
with open(in_file, 'rb') as file:
    a=bytearray(file.read())

with open(out_file,'w') as file:
    file.write(a)
image = Image.open(io.BytesIO(a))
image.show()


