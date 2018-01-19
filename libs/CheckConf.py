#!/usr/bin/env python3
from .appjar0830 import gui 
import os
from .BlueFunc import *
from .debug import * 

DataFile = "DATA/DATA"

# LANGUAGE
LANGUAGE = BlueLoad("LANG", DataFile)
Debug("LANGUAGE : " + str(LANGUAGE))

def ChangeLanguage(btn):
	print("ChangeLanguage")
	BlueSave("LANG", LanguageList[app.getListBox("ListLanguage")[0]], DataFile)
	app.stop()

if LANGUAGE == None:
	app = gui("Configuration", "500x500") 
	LanguageList = {"Deutsch":"DE"}
	app.addLabel("Title", "Choose your Language :")
	app.addListBox("ListLanguage", LanguageList)
	app.addButton("Select", ChangeLanguage)
	app.go()
