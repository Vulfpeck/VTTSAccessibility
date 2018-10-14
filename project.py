"""Get the current mouse position."""

import logging
import sys
import time
import pyautogui
from win32api import GetSystemMetrics
from pynput import mouse
from PIL import Image
import pytesseract
import argparse
import os

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def getMousePosition():
    """
    Get the current position of the mouse.

    Returns
    -------
    dict :
        With keys 'x' and 'y'
    """
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
    mouse_coordinates = getMousePosition()

    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    screenshotLocationX = mouse_coordinates['x'] - 250
    screenshotLocationY = mouse_coordinates['y'] -100

    if (screenshotLocationX + 500 > screenWidth ):
        screenshotLocationX = screenWidth - 500;
    


    im = pyautogui.screenshot("screen_region.jpg", region=(
        screenshotLocationX, screenshotLocationY, 500, 200))
    im.show()

def getScreenAreaLarge():
    initLoc = ()
    finalLoc = ()

    def on_click(x, y, button, pressed):
        if pressed:
            nonlocal initLoc
            initLoc = (x,y)
        else:
            nonlocal finalLoc
            finalLoc = (x,y)
        if not pressed:
            # Stop listener
            return False

    # Collect events until released
    with mouse.Listener(
            on_click=on_click,) as listener:
        listener.join()
    
    
    print(initLoc)
    print(finalLoc)

    screenshotLocationX = initLoc[0]
    screenshotLocationY = initLoc[1]

    screenShotWidth = abs(initLoc[0] - finalLoc[0])
    screenShotheight = abs (initLoc[1] - finalLoc[1])
    
    im = pyautogui.screenshot(region=(screenshotLocationX, screenshotLocationY, screenShotWidth, screenShotheight))
    im.show()


def ocrCapturedImage():
    #add code to ocr image here using pytesseract

def ttsTheText():
    #add code for tts here
getScreenAreaLarge()
ocrCapturedImage()
