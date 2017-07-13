#!/usr/bin/env python
from appJar import gui  
import os
import time
from KundenInfo import *
import pickle
import random
from BlueVar import *
from BlueFunc import *
from Data import *

app = gui("Kunden", "800x600")  
app.setLocation(1000, 200)

VERSION = BlueLoad("Version", "version")
Welcom = "By Zaunz Kenny \nVersion : " + str(VERSION) + "\nCopyright : Gnu GPL v3"
app.infoBox("KS", Welcom)

for directory in ["Arbeitskarten", "Kunden"]:
	BlueMkDir(directory)

for ESTRING in AlleDaten:
	if not ESTRING == "Notiz":
		app.addLabelEntry(ESTRING)
		app.setEntryDefault(ESTRING, ESTRING)

def KundenInfo(btn):
	print("KundenInfo")
	ID = app.getListItems("ListKunden")[0].partition(" ")[0]
	GetKundenInfo(ID)
	KundenSuchen("")

def KundenEntfernen(btn):
	print("KundenEntfernen")
	ID = app.getListItems("ListKunden")[0].partition(" ")[0]
	JA = app.yesNoBox("Loeschen...", "Sind sie sicher das sie den Kunden loeschen moechten?")
	
	if JA :
		os.remove("Kunden/" + str(ID))
		KundenSuchen("")

def KundenNeu(btn):
	print("KundenNeu")
	KundeID = 0
	while True:
		if not os.path.exists("Kunden/" + str(KundeID)): break
		else: KundeID = KundeID + 1
	
	print("Add " + str(KundeID))

	for DatenX in AlleDaten:
		DataToSave = app.textBox("Neuer Kunde", str(DatenX) + " : ")
		BlueSave(DatenX, DataToSave, "Kunden/" + str(KundeID))

	GetKundenInfo(KundeID)
	KundenSuchen("")

def KundenSuchen(btn):
	print("KundenSuchen")
	app.clearListBox("ListKunden")
	for Kunden in os.listdir("Kunden/"):
		DatenZumAnzeigen = Kunden
		Gefunden=True
		for DatenY in AlleDaten:
			if not DatenY == "Notiz":
				DatenZumAnzeigen = DatenZumAnzeigen + " " + str(BlueLoad(DatenY, "Kunden/" + Kunden))
				if not app.getEntry(DatenY).lower() in str(BlueLoad(DatenY, "Kunden/" + Kunden)).lower():
					Gefunden=False
		if Gefunden:
			app.addListItem("ListKunden", DatenZumAnzeigen)

app.addButton("Suchen", KundenSuchen)
app.addListBox("ListKunden")
app.addButton("Info", KundenInfo)
app.addButton("Neu", KundenNeu)
app.addButton("Entfernen", KundenEntfernen)
app.bindKey("<Return>", KundenSuchen)

app.go()  
