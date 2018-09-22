/*ran npm install --global --production windows-build-tools in cmd as an admin before 
*/
var midi = require('midi')
var launchpadder = require('launchpadder')
var launchpad = launchpadder.Launchpad
var cmd = require('node-cmd')
var output = new midi.output();
var sleep = require('sleep').sleep

var blank=[
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]   
]
var transform=[[0,1,2,3,4,5,6,7],
[16,17,18,19,20,21,22,23],
[32,33,34,35,36,37,38,39],
[48,49,50,51,52,53,54,55],
[64,65,66,67,68,69,70,71],
[80,81,82,83,84,85,86,87],
[96,97,98,99,100,101,102,103],
[112,113,114,115,116,117,118,119]]

function append(lettera,letterb){
    r=blank.slice(0,blank.length)
    for (var i=0; i<8; i++){
        r[i]=lettera[i].concat(letterb[i])
    }
    return r
}

function convert_string(someString){
    var a=[
    [0,0,0,1,1,0,0,0],
    [0,0,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,0],
    [1,1,1,0,0,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,1],
    [1,1,1,0,0,1,1,1],
    [1,1,1,0,0,1,1,1]
    ]
    var b=[
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0]   
    ]
    var c=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    var d=[
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,0,0,0,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,0,0]   
    ]
    var e=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]   
    ]
    var f=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0]  
    ]
    var g=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    var h=[
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1]
    ]
    var i=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]   
    ]
    var j=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [1,1,0,1,1,0,0,0],
        [1,1,1,1,1,0,0,0],
        [1,1,1,1,1,0,0,0]   
    ]
    var k=[
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,1,1,1,0],
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,0,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1]
    ]
    var l=[
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],    
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]   
    ]
    var m=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    var n=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,0,1,1],
        [1,1,1,1,0,0,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    var o=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    var p=[
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0] 
    ]
    var q=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,1,0,1,1],
        [1,1,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1]   
    ]
    var r=[
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1] 
    ]
    var s=[
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    var t=[
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0]   
    ]
    var u=[
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0]   
    ]
    var v=[
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [0,1,1,0,0,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,0,1,1,0,0,0]   
    ]
    var w=[
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    var x=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,1,1,1],
        [0,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1],
        [1,1,0,0,0,0,1,1]  
    ]
    var y=[
        [1,1,0,0,0,0,1,1],
        [1,1,1,0,0,1,1,1],
        [0,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0]
    ]
    var z=[
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
    for (var i =0; i<someString.length; i++){
        if (someString[i]=='a'){
            vector.push(a)}
        else if (someString[i]=='b'){
            vector.push(b)}
        else if (someString[i]=='c'){
            vector.push(c)}
        else if (someString[i]=='d'){
            vector.push(d)}
        else if (someString[i]=='e'){
            vector.push(e)}
        else if (someString[i]=='f'){
            vector.push(f)}
        else if (someString[i]=='g'){
            vector.push(g)}
        else if (someString[i]=='h'){
            vector.push(h)}
        else if (someString[i]=='i'){
            vector.push(i)}
        else if (someString[i]=='j'){
            vector.push(j)}
        else if (someString[i]=='k'){
            vector.push(k)}
        else if (someString[i]=='l'){
            vector.push(l)}
        else if (someString[i]=='m'){
            vector.push(m)}
        else if (someString[i]=='n'){
            vector.push(n)}
        else if (someString[i]=='o'){
            vector.push(o)}
        else if (someString[i]=='p'){
            vector.push(p)}
        else if (someString[i]=='q'){
            vector.push(q)}
        else if (someString[i]=='r'){
            vector.push(r)}
        else if (someString[i]=='s'){
            vector.push(s)}
        else if (someString[i]=='t'){
            vector.push(t)}
        else if (someString[i]=='u'){
            vector.push(u)}
        else if (someString[i]=='v'){
            vector.push(v)}
        else if (someString[i]=='w'){
            vector.push(w)}
        else if (someString[i]=='x'){
            vector.push(x)}
        else if (someString[i]=='y'){
            vector.push(y)}
        else if (someString[i]=='z'){
            vector.push(z)}
        else if (someString[i]==' '){
            vector.push([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
        }
    }
    new_matrix=blank.slice(0,blank.length)
    for (var i = 0; i< vector.length;i++){
        new_matrix=append(new_matrix,vector[i])
        new_matrix=append(new_matrix,[[0],[0],[0],[0],[0],[0],[0],[0]])
    }
    new_matrix=append(new_matrix,blank.slice(0,blank.length))
    return new_matrix
}
function target_process(i,j,brightness){
    num=transform[i][j]
    output.sendMessage([144,num,brightness])
}
function led_out(window,num){
    for (var i=0; i<8; i++){
        for (var j=0; j<8; j++){
            if(window[i][j]==1){ 
                target_process(i,j,num)
            }
        }
    }
}
function led_off(){
    for (var i; i<128; i++){
        output.sendMessage([144,i,0])
    }
}
function added_window(window,pastwindow){
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

    for (var i=0; i<8; i++){
        for (var j=0; j<8; j++){
            if (window[i][j]==0){
                if(pastwindow[i][j]==1){
                    added[i].push(1)
                }
                else if(pastwindow[i][j]==0){
                    added[i].push(0)
                }
            }
            else if (window[i][j]==1){
                if(pastwindow[i][j]==1){
                    added[i].push(1)
                }
                else if(pastwindow[i][j]==0){
                    added[i].push(1)
                }
            }
        }
    }
    return added
}
function difference_window(window,pastwindow){
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
    for (var i=0; i<8; i++){
        for (var j=0; j<8; j++){
            if (window[i][j]==0){
                if(pastwindow[i][j]==1){
                    must_erase[i].push(1)
                }
                else if(pastwindow[i][j]==0){
                    must_erase[i].push(0)
                }
            }
            else if (window[i][j]==1){
                if(pastwindow[i][j]==1){
                    must_erase[i].push(0)
                }
                else if(pastwindow[i][j]==0){
                    must_erase[i].push(0)
                }
            }
        }
    }
    return must_erase
}
    

function findLaunchpadPort () {
    
    for (var i = 0; i < output.getPortCount(); i++) {
        
        try{
            console.log(output.getPortName(i).match('Launchpad Mini')[0]=='Launchpad Mini')
            if (output.getPortName(i).match('Launchpad Mini')[0]=='Launchpad Mini'){
                return i
            }
        }
        catch(e){
            console.log('not it')
        }
  }
}
var portnum=findLaunchpadPort();
console.log(portnum);
output.openPort(portnum);
function marquee(word){
    matrix=convert_string(word)
    window=blank.slice(0,blank.length)
    for (var i=0; i<8; i++){
        window[i]=matrix[i].slice(0,8)
    }
    
    past_window=window.slice(0,window.length)
    for (var i=0; i<matrix[0].length-7; i++){
        led_off()
        led_out(added_window(window,past_window),127)
        
        led_out(difference_window(window,past_window),0)
        past_window=window.slice(0,window.length)
        for (var j =0; j<8; j++){
            window[j].pop(0)
            window[j].push(matrix[j][i+7])
        }
    }
}
marquee('biz marquee')