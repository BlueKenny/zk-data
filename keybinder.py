#!/usr/bin/env python

import pyautogui

def Click():
	print("Click")
	pyautogui.click()
def Maus(x, y):
	print("Maus x:" + str(x) + " y:" + str(y))
	pyautogui.moveTo(x, y)
def Key(key):
	pyautogui.hotkey(key)
def Write(key):
	pyautogui.typewrite(str(key))
