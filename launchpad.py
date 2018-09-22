#pip install python-rtmidi
import rtmidi
import time
import multiprocessing
import sys
from rtmidi.midiutil import open_midioutput

midiout=rtmidi.MidiOut()
for portnum in range(len(midiout.get_ports())):
    if 'Launchpad Mini' in midiout.get_ports()[portnum]:
        LPport=portnum
midiout.open_port(LPport)
note_on=[0x90,64,127]
note_off=[0x90,64,0]
transform=[[0,1,2,3,4,5,6,7],
[16,17,18,19,20,21,22,23],
[32,33,34,35,36,37,38,39],
[48,49,50,51,52,53,54,55],
[64,65,66,67,68,69,70,71],
[80,81,82,83,84,85,86,87],
[96,97,98,99,100,101,102,103],
[112,113,114,115,116,117,118,119]]
blank=[
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]   
]

def led_off():
    for i in range(128):
        midiout.send_message([0x90,i,0])

def target_process(i,j,brightness):
    num=transform[i][j]
    midiout.send_message([0x90,num,brightness])

def led_dim(window,num):
    for i in range(8):
        for j in range(8):
            if(window[i][j]==1):    
                target_process(i,j,num)


def led_on(window):
    for i in range(8):
        for j in range(8):
            if(window[i][j]==1):    
                
                target_process(i,j,127)
                
                """
                p=multiprocessing.Process(target=target_process, args=(i,j))
                p.start()
                p.join()
                """
                

        

def append(lettera,letterb):
    r=blank.copy()
    for i in range(8):
        r[i]=lettera[i]+letterb[i]
    
    return r
def convert_string(some_string):
    a=[
    [0,0,0,1,1,0,0,0],
    [0,0,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,0],
    [1,1,1,0,0,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,1],
    [1,1,1,0,0,1,1,1],
    [1,1,1,0,0,1,1,1]
    ]
    b=[
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0]   
    ]
    c=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    d=[
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,0,0,0,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,0,0]   
    ]
    e=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]   
    ]
    f=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0]  
    ]

    g=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]

    h=[
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1]
    ]
    i=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]   
    ]
    j=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [1,1,0,1,1,0,0,0],
        [1,1,1,1,1,0,0,0],
        [1,1,1,1,1,0,0,0]   
    ]
    k=[
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,1,1,1,0],
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,0,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1]
    ]
    l=[
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],    
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]   
    ]
    m=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    n=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,0,1,1],
        [1,1,1,1,0,0,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    o=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    p=[
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0] 
    ]
    q=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,1,0,1,1],
        [1,1,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1]   
    ]
    r=[
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1] 
    ]
    s=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    t=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0]   
    ]
    u=[
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    v=[
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [0,1,1,0,0,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,0,1,1,0,0,0]   
    ]
    w=[
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    x=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,1,1,1],
        [0,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    y=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,1,1,1],
        [0,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0]
    ]
    z=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,0,1,1,1,0],
        [0,0,0,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]  
    ]
    vector=[]
    for letter in list(some_string):
        if letter=='a':
            vector.append(a)
        elif letter=='b':
            vector.append(b)
        elif letter=='c':
            vector.append(c)
        elif letter=='d':
            vector.append(d)
        elif letter=='e':
            vector.append(e)
        elif letter=='f':
            vector.append(f)
        elif letter=='g':
            vector.append(g)
        elif letter=='h':
            vector.append(h)
        elif letter=='i':
            vector.append(i)
        elif letter=='j':
            vector.append(j)
        elif letter=='k':
            vector.append(k)
        elif letter=='l':
            vector.append(l)
        elif letter=='m':
            vector.append(m)
        elif letter=='n':
            vector.append(n)
        elif letter=='o':
            vector.append(o)
        elif letter=='p':
            vector.append(p)
        elif letter=='q':
            vector.append(q)
        elif letter=='r':
            vector.append(r)
        elif letter=='s':
            vector.append(s)
        elif letter=='t':
            vector.append(t)
        elif letter=='u':
            vector.append(u)
        elif letter=='v':
            vector.append(v)
        elif letter=='w':
            vector.append(w)
        elif letter=='x':
            vector.append(x)
        elif letter=='y':
            vector.append(y)
        elif letter=='z':
            vector.append(z)
        elif letter==' ':
            vector.append([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
    new_matrix=blank.copy()
    for i in range(len(vector)):
        new_matrix=append(new_matrix,vector[i])
        #new_matrix=vector[i].copy()
        new_matrix=append(new_matrix,[[0],[0],[0],[0],[0],[0],[0],[0]])
    new_matrix=append(new_matrix,blank.copy())
    return new_matrix

def added_window(window,pastwindow):
    added=[
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []   
]
    for i in range(8):
        for j in range(8):
            if (window[i][j]==0):
                if(pastwindow[i][j]==1):
                    added[i].append(1)
                elif(pastwindow[i][j]==0):
                    added[i].append(0)
            elif (window[i][j]==1):
                if(pastwindow[i][j]==1):
                    added[i].append(1)
                elif(pastwindow[i][j]==0):
                    added[i].append(1)
    return added

def difference_window(window,pastwindow):
    must_erase=[
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []   
]
    for i in range(8):
        for j in range(8):
            if (window[i][j]==0):
                if(pastwindow[i][j]==1):
                    must_erase[i].append(1)
                elif(pastwindow[i][j]==0):
                    must_erase[i].append(0)
            elif (window[i][j]==1):
                if(pastwindow[i][j]==1):
                    must_erase[i].append(0)
                elif(pastwindow[i][j]==0):
                    must_erase[i].append(0)
    return must_erase


def marquee(word):
    matrix=convert_string(word)
    for i in range(len(matrix[0])-8):
        past_window=matrix.copy()
        for j in range(8):
            matrix[j].pop(0)
            matrix[j].append(matrix[j][i+7])
        #led_dim(past_window,127)
        led_dim(added_window(matrix,past_window),127)
        led_dim(difference_window(matrix,past_window),0)
       
        

        
        


if __name__ == "__main__":
    if len(sys.argv)<2:
        raise SyntaxError("Please Provide a Keyword as an argument")
    else:
        words=""
        for i in range(len(sys.argv)-1):
            print(sys.argv[i+1])
        marquee(str(sys.argv[1]))