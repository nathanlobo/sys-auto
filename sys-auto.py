import pyautogui as gui
import time
import pygame

# Use SELENIUM

def find_Chat(text):
    # gui.hotkey('ctrl','f')
    gui.write(text)
    # time.sleep()

def openChat():
    gui.press("tab")
    gui.press("enter")
    gui.click(858, 706)
    time.sleep(.5)

def t():
    time.sleep(1)

def playmp3(filename):
    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(filename=filename)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

gui.KEY_NAMES()
gui.hotkey("windows", "d")
gui.write("whatsapp")
t()
gui.press("enter")
t()
# find_Chat("chaitali")
# openChat()

# gui.write("Good evening sis", interval=0.2)
# gui.press("enter")
# gui.hotkey('ctrl','f')
# t()
# gui.press("tab",presses=8,interval=.2)
# t()
# gui.hotkey('shift', 'f10') # Shift + F10 to right click
# t()
# gui.press("down",presses=2,interval=1)
# playmp3("BEEP.mp3"dwhatsapp
)
# gui.press("enter")
# with open("msgs.txt", 'a') as f:
#     f.write(f"\n{session_id}")

