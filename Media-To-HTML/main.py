import argparse
import glob
import base64
from bs4 import BeautifulSoup
import pathlib
import os
import random

parser = argparse.ArgumentParser()

parser.add_argument('--images', help="Root directory containing images", type=str)
parser.add_argument('--directory','-d', help="Directory to store html file", default=os.getcwd(), type=str)

args = vars(parser.parse_args())

html = BeautifulSoup("<!DOCTYPE html><html><head></head><body></body></html>", 'html.parser')
css = html.new_tag('style')
with open("style.css", 'r') as f:
    css.string = f.read()
html.find('head').append(css)
body = html.find("body")
images = []
for i in ('.png', '.jpg', '.gif'):
    images.extend(glob.glob(args['images']+'/*'+i))

random.shuffle(images)
leng = len(images)

row = html.new_tag('div')
row['class'] = 'row'

col1 = html.new_tag('div')
col2 = html.new_tag('div')
col3 = html.new_tag('div')
col4 = html.new_tag('div')

col1['class'] = 'column'
col2['class'] = 'column'
col3['class'] = 'column'
col4['class'] = 'column'


for i in range(leng): 
    if i < leng/4:
        tempdiv = col1
    elif i < leng/2:
        tempdiv = col2
    elif i<3*leng/4:
        tempdiv = col3
    else:
        tempdiv = col4
        
    with open(images[i], 'rb') as img:
        ext = pathlib.Path(images[i]).suffix[1::]
        string = ""
        with open('temp.txt', 'wb') as t:
            t.write(base64.b64encode(img.read()))
        with open('temp.txt', 'r') as t:
            string = t.read()
        img = html.new_tag('img')
        img['src'] = 'data:image/'+ext+';base64,'+string
        tempdiv.append(img)

row.append(col1)
row.append(col2)
row.append(col3)
row.append(col4)

body.append(row)

with open("test.html", 'w') as f:
    f.write(str(html.prettify()))
