
import logging
import sys
import time
import pyautogui
from win32api import GetSystemMetrics
from pynput import mouse
from PIL import Image, ImageEnhance
import pytesseract
import argparse
import cv2
import os
from gtts import gTTS       
import string

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def getMousePosition():
    # this is the platform specific code, mainly designed for Windows
    # it's primary purpose is the return a tuple containing the x&y coordinates
    # of the mouse when requested at a specific time
    # however, it does not have methods for on click events and is used
    # in odd cases where other method does not work
    
    mouse_position = None
    
    import sys
    if sys.platform in ['linux', 'linux2']:
        pass
    elif sys.platform == 'win32':
        try:
            import win32api
        except ImportError:
            logging.info("win32api not installed")
            win32api = None
        if win32api is not None:
            x, y = win32api.GetCursorPos()
            mouse_position = {'x': x, 'y': y}
    elif sys.platform == 'Mac':
        pass
    else:
        try:
            import Tkinter  # Tkinter could be supported by all systems
        except ImportError:
            logging.info("Tkinter not installed")
            Tkinter = None
        if Tkinter is not None:
    
            p = Tkinter.Tk()
            x, y = p.winfo_pointerxy()
            mouse_position = {'x': x, 'y': y}
    
        print("sys.platform={platform} is unknown. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    return mouse_position


def getScreenAreaStripe():
    # get mouse cursor coordinates from the libraries
    mouse_coordinates = getMousePosition()

    # get screen width and height from win32api
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    # center the screenshot relative to the mouse cursor location
    screenshotLocationX = mouse_coordinates['x'] - 250
    screenshotLocationY = mouse_coordinates['y'] -100

    # if location surpases the edge of the screen
    if (screenshotLocationX + 500 > screenWidth ):
        screenshotLocationX = screenWidth - 500;
    

    #take screenshot and save it for future processing
    im = pyautogui.screenshot("screen_region.jpg", region=(
        screenshotLocationX, screenshotLocationY, 500, 200))
    # print(type(im))
    return im

def getOnclickLocation():
    clickLoc = ()

    def on_click(x, y, button, pressed):
        # default action when mouse primary button is clicked
        if pressed:
            print('mouse clicked')
            # nonlocal allows to access the variable outside the scope
            # of function
            nonlocal clickLoc
            clickLoc = (x,y)

        
        if not pressed:
            # Stop listener
            return False

    # Collect events until released
    with mouse.Listener(
            on_click=on_click,) as listener:
        listener.join()
    
    return clickLoc
    # print(initLoc)
    # print(finalLoc)

    # screenshotLocationX = initLoc[0]
    # screenshotLocationY = initLoc[1]

    # screenShotWidth = abs(initLoc[0] - finalLoc[0])
    # screenShotheight = abs (initLoc[1] - finalLoc[1])
    
    # im = pyautogui.screenshot("screen_region.jpg", region=(screenshotLocationX, screenshotLocationY, screenShotWidth, screenShotheight))
    # im.show()

def getScreenAreaLarge():
    # get initial click event
    clickLocInit = getOnclickLocation()
    # get second click event
    clickLocFinal = getOnclickLocation()

    print(clickLocInit)
    print(clickLocFinal)
    
    # calculate position for the screenshot
    screenshotLocationX = clickLocInit[0]
    screenshotLocationY = clickLocInit[1]
    
    screenShotWidth = abs(clickLocInit[0] - clickLocFinal[0])
    screenShotHeight = abs (clickLocInit[1] - clickLocFinal[1])

    im = pyautogui.screenshot("screen_region.jpg", region=(screenshotLocationX, screenshotLocationY, screenShotWidth, screenShotHeight))
    return im

def ocrCapturedImage():

    image = cv2.imread('screen_region.jpg')
    # process image for pytesseract
    gray = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 150, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite('processed.jpg', gray)

    im = Image.open('processed.jpg')
    # run pytesseract
    ocrText = (pytesseract.image_to_string(im, lang='eng',config='--psm 1'))

    ocrText = ocrText.replace('\n', ' ')
    return ocrText

def textToSpeech():
    # get the text
    text = ocrCapturedImage()
    print(text)
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    # speak the text
    engine.runAndWait()  

getScreenAreaLarge()
textToSpeech()