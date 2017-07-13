#!/usr/bin/env python
#from pynput import *
from pynput.mouse import *
#from pynput.keyboard import *

def Click():
	print("Click")
	Controller().press(Button.left)
	Controller().release(Button.left)
def Maus(x, y):
	print("Maus x:" + str(x) + " y:" + str(y))
	Controller().position = (int(x), int(y))
def Key(key):
	print("Key " + str(key))
	Controller().press(str(key))
	Controller().release(str(key))
def Write(text):
	print("Type " + str(key))
	Controller().type(str(text))

def Pos():
	print(Controller().position)
