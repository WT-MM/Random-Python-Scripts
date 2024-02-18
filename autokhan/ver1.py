import pyautogui
import keyboard

'''
Note all positions were hardcoded with full screen khanacademy and my macbook pro in mind
'''

tryAgain = (492, 869)
LetsGo = (1377, 860)
a = (714, 490)
b = (714, 560)
c = (714, 612)

top = (714, 470)
bottom = (714, 660) #For three
bottom = (714, 620) #For two


def printCurrentMousePosition():
    if(keyboard.is_pressed('s')):
        print(pyautogui.position())


def checkQuit():
    return keyboard.is_pressed('q')

def doubleClick(loc):
    pyautogui.click(loc)
    pyautogui.click(loc)

def doubleClickLower(loc):
    higher = (loc[0], loc[1] - 10)
    pyautogui.click(higher)
    #pyautogui.click(loc)
    lower = (loc[0], loc[1] + 10)
    pyautogui.click(lower)
    
def clickInRange(start, end, steps):
    for i in range(start[1], end[1], steps):
        clickLoc = (start[0], i)
        pyautogui.click(clickLoc)
        doubleClick(LetsGo)
        pyautogui.PAUSE = 0.9
        pyautogui.click(tryAgain)
        if(checkQuit()): return

#Begin inside the practice page
def autoAnswer():
    if(begin):
        clickInRange(top, bottom, 30)

        if(checkQuit()): return


begin = False

while True:
    if(checkQuit()):
        break
    if(keyboard.is_pressed('b')):
        begin = True
   # printCurrentMousePosition()
    autoAnswer()
