import glob
import random

class Retrieve:
    
    def __init__(self, addr):
        self.rootDir = addr
        self.findImgs()
        

    def findImgs(self, shuffle=True):
        self.imgs = []
        for i in ('.png', '.jpg', '.gif'):
            imgs.extend(glob.glob(args['images']+'/*'+i))
        
        if(shuffle):
            random.shuffle(imgs)

    def returnImgs(self):
        return self.imgs
