#!/usr/bin/python2.7

from google.cloud import vision
from google.cloud.vision import types
from Xlib import display, X
from PIL import Image
import io
import re
import requests
import json

def test_srch():
    q = "What kind of writing is rewarded with a Hugo Awars"
    opts = ["science-fiction","horror-fiction","Expedition Robinson"]
    cnts = goog_srch(q,opts)

def test_img():
    img = screen_shot()
    img.show()

def setup():
    global goog_vclient
    global goog_cse
    
    goog_vclient = vision.ImageAnnotatorClient()

    cse = open("../keys/cse_key.json").read()
    cse = json.loads(cse)

    goog_cse = ("https://www.googleapis.com/customsearch/v1?" + "&" +
                "key=" + cse["api_key"]                       + "&" +
                "cx="  + cse["cse_id"]                        + "&")
    

def goog_srch(q,opts):
    query = "q=" + q

    resp = requests.get(goog_cse + query)
    resp = resp.text.encode('utf8','replace').splitlines()

    print resp
    
    cnt = {}
    for opt in opts:
        cnt[opt] = 0
        
    for line in resp:            
        for opt in opts:
            if(re.match(".*\-",opt)):
                s_opt = opt.split("-")
                for o in s_opt:
                    if(re.match(".*\s+" + o + "\s+.*",line,re.IGNORECASE)):
                        cnt[opt] += 1
            else:
                if(re.match(".*\s+" + opt + "\s+.*",line,re.IGNORECASE)):
                    cnt[opt] += 1

    for opt in opts:
        print opt + ":" + str(cnt[opt])

                
def get_text():    
    img    = screen_shot()
    img_ba = io.BytesIO()
    img.save(img_ba,format='PNG')
    img_ba = img_ba.getvalue()

    image = types.Image(content=img_ba)
    response = goog_vclient.text_detection(image=image)
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

    goog_srch(q,opts)
        
def screen_shot():
    _w,_h = 270,230
    _x,_y = 390,280
    dsp   = display.Display()
    root  = dsp.screen().root
    raw   = root.get_image(_x,_y,_w,_h,X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (_w, _h), raw.data, "raw", "BGRX")
    return image
    
if __name__ == '__main__':
    setup()
    test_srch()
    #test_img()    
    '''
    inp = ''
    while True:
        inp = raw_input('< : ')
        if(inp == 'x'):
            break
        get_text()

    '''
