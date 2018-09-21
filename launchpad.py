#pip install python-rtmidi
import rtmidi
import time

midiout=rtmidi.MidiOut()
for portnum in range(len(midiout.get_ports())):
    if 'Launchpad Mini' in midiout.get_ports()[portnum]:
        LPport=portnum
midiout.open_port(LPport)
note_on=[0x90,64,127]
note_off=[0x90,64,0]
matrix=[[0,1,2,3,4,5,6,7],
[16,17,18,19,20,21,22,23],
[32,33,34,35,36,37,38,39],
[48,49,50,51,52,53,54,55],
[64,65,66,67,68,69,70,71],
[80,81,82,83,84,85,86,87],
[96,97,98,99,100,101,102,103],
[112,113,114,115,116,117,118]]

for i in range(128):
    midiout.send_message([0x90,i,0])

while(True):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            note_on[1]=matrix[i][j]
            note_off[1]=matrix[i][j]
            midiout.send_message(note_on)
            time.sleep(0.01)
            midiout.send_message(note_off)
            time.sleep(0.01)
    #print(note_on[1])

