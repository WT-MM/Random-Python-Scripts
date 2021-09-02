import glob
import random

class Retrieve:
    
    def __init__(self, addr, shuffle=True, rootLevel=True):
        self.rootDir = addr
        self.rootLevel = rootLevel
        self.shuffle = shuffle
        

    def findImgs(self):
        self.imgs = []
        search = ['/*.png','/*.jpg','/*.jpeg','/*.gif']

        self.imgs = self.baseRetrieve(search)

    def getImgs(self):
        if(not self.imgs):
            self.findImgs()
        return self.imgs
    
    def baseRetrieve(self, search:
        if(not self.rootLevel):
            search = ['/*' + i for i in search]
        
        tempMedia = []

        for i in search:
            tempMedia.extend(glob.glob(self.rootDir+i))

        if(self.shuffle):
            random.shuffle(tempMedia)
        
        return tempMedia
    def findAudio(self):
        self.audio = []
        search = ["", ""]
        self.audio = self.baseRetrieve(search)

    def getAudio(self):
        if(not self.audio):
            self.findAudio()
        return self.audio