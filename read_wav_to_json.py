from scipy.io.wavfile import read
a=read('white_noise.wav')
import json
import numpy as np 
b=[]
for i in range(len(a[1])):
    b.append(a[1][i][0])

c=np.asarray(b)
d=c.tolist()
e=json.dumps(d)

file =open('white_noise.json','w')
file.write(e)
file.close()
