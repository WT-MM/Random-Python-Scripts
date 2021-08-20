import argparse
import glob
import base64
from bs4 import BeautifulSoup
import pathlib
import os
import random
import threading
import time


parser = argparse.ArgumentParser()

parser.add_argument('--images', help="Root directory containing images", type=str)
parser.add_argument('--directory','-d', help="Directory to store html file", default=os.getcwd(), type=str)
parser.add_argument('--name', help="Name of HTML file", default="1", type=str)

args = vars(parser.parse_args())

#Base html
html = BeautifulSoup("<!DOCTYPE html><html><head></head><body></body></html>", 'html.parser')
css = html.new_tag('style')

#Read in css from .css file
with open("style.css", 'r') as f:
    css.string = f.read()

html.find('head').append(css)

body = html.find("body")

#Find all images in provided directory
imgs = []
for i in ('.png', '.jpg', '.gif'):
    imgs.extend(glob.glob(args['images']+'/*'+i))

random.shuffle(imgs)

#Basic img gallery markup
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

cols = [col1,col2,col3,col4]


def bulkEncode(section, id):
    temptxt = str(id) +'.txt'
    #Iterate through each img path
    for i in section:
        with open(i, 'rb') as img:
            #Extract file type from name
            ext = pathlib.Path(i).suffix[1::]
            string = ""

            #Write bytes to txt (find better solution)
            with open(temptxt, 'wb') as t:
                t.write(base64.b64encode(img.read()))
            #Read txt as string
            with open(temptxt, 'r') as t:
                string = t.read()
            img = html.new_tag('img')
            img['src'] = 'data:image/'+ext+';base64,'+string
            cols[id].append(img)
    #Delete temporary txt file
    os.remove(temptxt)
    print("Col " + str(id) + " completed")

def threaded(images):
    #Create threads
    t1 = threading.Thread(target=bulkEncode, args=(images[0::4],0))
    t2 = threading.Thread(target=bulkEncode, args=(images[1::4],1))
    t3 = threading.Thread(target=bulkEncode, args=(images[2::4],2))
    t4 = threading.Thread(target=bulkEncode, args=(images[3::4],3))

    #Start thread execution
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    #Wait for threads to finish
    t1.join()
    t2.join()
    t3.join()
    t4.join()

def nonThreaded(images):
    leng = len(images)
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
    os.remove("temp.txt")

'''
nS = time.time()
nonThreaded(imgs)
nTime = str(time.time() - nS)

tS = time.time()
threaded(imgs)
tTime = str(time.time() - tS)
print("Non Threaded Time: " + nTime + "\nThreaded Time: " + tTime)
'''

threaded(imgs)


row.append(col1)
row.append(col2)
row.append(col3)
row.append(col4)

body.append(row)

print("Creating HTML File")
with open(args['name']+".html", 'w') as f:
    f.write(str(html.prettify()))

