from moviepy.editor import *
import moviepy
start=(11.00)
stop=(12.00)
clip="IMG_0219.MOV"
out="test.gif"
clip1 = (VideoFileClip(clip).subclip((start),(stop)).resize(0.5))
clip2=moviepy.video.fx.all.time_symmetrize(clip1)
clip3=clip2.crop(y1=128,y2=952)
clip3.write_gif(out,fps=15)

