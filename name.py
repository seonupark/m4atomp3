from moviepy.editor import *
import os
from PIL import Image, ImageDraw, ImageFont


file_list = os.listdir()
file_name=[]
for file in file_list:
    if file.split('.')[-1] == "m4a":
        name = file.split('.')[:-1]
        file_name.append(name)
    else:
        pass

for ff in file_name:
    im = Image.open("black.png")
    draw = ImageDraw.Draw(im)
    draw.text((100, 400),str(ff)[2:-2], font=ImageFont.truetype("HMKMRHD.TTF", 80), fill=(255, 255, 255))
    im.save(str(ff)[2:-2]+".png")
