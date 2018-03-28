#!/usr/bin/python2.7

from google.cloud import vision
from google.cloud.vision import types
from Xlib import display, X
from PIL import Image
import io
import re

def get_text(picture):    
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=picture)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    q = ""
    o = 0    
    opts = []
    neg = 0

    texts = texts[0].description.splitlines()
    
    for text in texts:
        if not o:
            if(re.match(".*NOT",text)):
                neg = 1
            if(re.match(".*\?",text)):
                q = q + " " + text
                o = 1
            else:
                q = q + " " + text
        else:
            opts.append(text)
            
    print "Q " + q
    print "options " + str(opts)
    print "neg " + str(neg)
        
def screen_shot():
    _w,_h = 250,230
    _x,_y = 530,270
    dsp   = display.Display()
    root  = dsp.screen().root
    raw   = root.get_image(_x,_y,_w,_h,X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (_w, _h), raw.data, "raw", "BGRX")
    img_ba= io.BytesIO()
    image.save(img_ba,format='PNG')
    img_ba= img_ba.getvalue()
    get_text(img_ba)
    #image.show()
    
if __name__ == '__main__':
    key = ''
    while True:
        key = raw_input('< : ')
        if(key == 'x'):
            break
        screen_shot()

