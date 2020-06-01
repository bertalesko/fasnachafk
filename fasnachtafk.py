import ctypes
import datetime
import schedule
from pynput.keyboard import Controller
import time

keyboard = Controller()  # Create the controller

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



def enter():
    for x in range(5):
        PressKey(0x1c)
        time.sleep(0.1)
        ReleaseKey(0x1c)
        time.sleep(0.1)
    
    now = datetime.datetime.now()
    print("enter : "+ now.strftime("%Y-%m-%d %H:%M:%S"))

def antiafk():


    PressKey(0x11)
    time.sleep(0.1)
    ReleaseKey(0x11)
    time.sleep(0.1)
    PressKey(0x1F)
    time.sleep(0.1)
    ReleaseKey(0x1F)
    now = datetime.datetime.now()
    print("moved : "  + now.strftime("%Y-%m-%d %H:%M:%S"))


schedule.every(1).minutes.do(antiafk)
schedule.every(1).minutes.do(enter)


while True:
    schedule.run_pending()
    time.sleep(1)
