#!/usr/bin/python2.7

from google.cloud import vision
from google.cloud.vision import types
from Xlib import display, X
import Image
import io

def get_text(picture):    
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=picture)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    
    for text in texts:
        print('\n"{}"'.format(text.description))
        
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

def screen_shot():
    W,H   = 250,230
    dsp   = display.Display()
    root  = dsp.screen().root
    raw   = root.get_image(1090, 350, W,H, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (W, H), raw.data, "raw", "BGRX")
    img_ba= io.BytesIO()
    image.save(img_ba,format='PNG')
    img_ba= img_ba.getvalue()
    get_text(img_ba)
    image.show()
    
if __name__ == '__main__':
    image = screen_shot()
    
