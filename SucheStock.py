#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
# Lieferant
EntryList=["Bcode", "Artikel", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Stock Suche", "800x600") 

def tbFunc(btn):
	Debug("btn : " + btn)

tools = ["NEU", "LÖSCHEN"]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addLabelEntry("Bcode")
appSuche.addLabelEntry("Artikel")
appSuche.addListBox("Suche")

def Suche(btn):
	Debug("Suche")

#appSuche.bindKey("<Return>", FuncSuche)
#appSuche.bindKey("<Escape>", FuncSave)


appSuche.addLabel("info", "Enter = Suche")
appSuche.bindKey("<Return>", Suche)
appSuche.go()
