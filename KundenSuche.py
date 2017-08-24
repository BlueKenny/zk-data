#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
from send import *

# appSuche definieren
appSuche = gui("Kunden", "800x600") 
# Version
Welcom = "By Zaunz Kenny \nVersion : " + str(BlueLoad("Version", "version")) + "\nCopyright : Gnu GPL v3"
appSuche.infoBox("KS", Welcom)
# SuchBox
EntryList = ["ID", "Name", "Tel", "Adr"]
for entry in EntryList:	
	appSuche.addLabelEntry(entry)
	appSuche.setEntryDefault(entry, entry)

def FuncSuchen(btn):
	Debug("FuncSuchen")
	appSuche.clearListBox("ListKunden")
	EntryIstLeer = False
	
	List = SearchKunden(appSuche.getEntry("ID"), appSuche.getEntry("Name"), appSuche.getEntry("Tel"), appSuche.getEntry("Adr"))

	for Linien in List.split("&K()K&"):
		Debug("Linien : " + str(Linien))
		addThis = Linien.split("&KK&")[0] + " | "+ Linien.split("&KK&")[1] + " | "+ Linien.split("&KK&")[2] + " | "+ Linien.split("&KK&")[3]
		appSuche.addListItem("ListKunden", addThis)

def FuncNeu(btn):
	Debug("FuncNeu")
	#	NeuerName
	NameRichtig = False
	while not NameRichtig:
		NeuerName = appSuche.textBox("Neuer Kunde :", "Achtung, Vor- und Nachname eingeben \nName : ")
		if len(NeuerName.split(" ")) > 1: NameRichtig = True
	NeuerName = NeuerName.title()
	Debug("NeuerName : " + NeuerName)
	#	NeueTel
	TelRichtig = False
	while not TelRichtig:
		NeueTel = appSuche.textBox("Neuer Kunde :", "Achtung, nur Zahlen eingeben \nMehrere Telefonnummern mit einem leerzeichen trennen \nTel : ")
		TelRichtig = True
		for e in NeueTel.split(" "):
			try: int(e); Debug("NeueTel : " + str(e))
			except : TelRichtig = False
	#	NeueAdr	
	AdrRichtig = False
	while not AdrRichtig:
		NeueAdr = appSuche.textBox("Neuer Kunde :", "Adresse : ")
		AdrRichtig = True
	NeueAdr = NeueAdr.title()
	Debug("NeueAdr : " + NeueAdr)	

	#	Kunde Speichern
	KundenID = AddKunde(NeuerName, NeueTel, NeueAdr)
	Debug("Neuer Kunde Gespeichert")
	appSuche.setEntry("ID", KundenID)
	appSuche.setEntry("Name", NeuerName)
	appSuche.setEntry("Tel", NeueTel)
	appSuche.setEntry("Adr", NeueAdr)
	FuncSuchen("")

def FuncEnter(btn):
	Debug("FuncEnter")
	try:
		SelectedID = appSuche.getListItems("ListKunden")[0].split(" | ")[0]
		FuncInfo(int(SelectedID))
	except: FuncSuchen("")

def FuncInfo(ID):
	Debug("FuncInfo : ID : " + str(ID))
	SelectedID = appSuche.getListItems("ListKunden")[0].split(" | ")[0]
	os.system("./KundenInfo.py " + str(SelectedID))

# Objecte erstellen
appSuche.addButton("Suchen", FuncSuchen)
appSuche.addListBox("ListKunden")
appSuche.addButton("Info", FuncInfo)
appSuche.addButton("Neu", FuncNeu)
# Tasten mit funktioennen verbinden
appSuche.bindKey("<Return>", FuncEnter)
# appSuche Starten
appSuche.go()  
