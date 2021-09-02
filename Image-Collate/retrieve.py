import glob
import random

class Retrieve:
    
    def __init__(self, addr):
        self.rootDir = addr
        self.findImgs()
        

    def findImgs(self, shuffle=True, rootLevel=True):
        self.imgs = []
        search = ['/*.png','/*.jpg','/*.jpeg','/*.gif']

        if(not rootLevel):
            search = ['/*' + i for i in search]


        for i in search:
            self.imgs.extend(glob.glob(self.rootDir+i))

        if(shuffle):
            random.shuffle(imgs)

    def getImgs(self):
        return self.imgs
