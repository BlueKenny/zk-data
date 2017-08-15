#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import subprocess
from random import randint
import socket

SERVER_IP = ("192.168.188.29", 10000)
s = socket.socket()
s.connect(SERVER_IP)

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
	for entry in EntryList:	
		BlueSave(entry, appSuche.getEntry(entry), TMP)
	BlueSave("Work", "Kunden", TMP)
	for z in os.listdir("Kunden/"):
		open(TMP + str(z) + "GO", "w").write(" ")
		subprocess.Popen(["./SucheProcess.py " + str(z)], shell = True)
	while True:
		Fertig = True
		for z in os.listdir("Kunden/"):
			if os.path.exists(TMP + str(z) + "GO"):
				Fertig = False
			else:
				if os.path.exists(TMP + str(z)):
					for KundeID in open(TMP + str(z), "r").readlines():
						KundeID = KundeID.rstrip()	
						KundenDatei =  "Kunden/" + KundeID[-1] + "/" + KundeID	
						addThis = str(KundeID)
						for Entry in EntryList:
							if not Entry == "ID":
								addThis = addThis + " | " + str(BlueLoad(Entry, KundenDatei))
						appSuche.addListItem("ListKunden",  addThis)
					os.remove(TMP + str(z))
		if Fertig: break
	print("FERTIG")

def FuncNeu(btn):
	Debug("FuncNeu")
	IDEnde = randint(int(IDMin), int(IDMax))
	Debug("IDEnde : " + str(IDEnde))
	KundenID = int(IDEnde)
	for x in os.listdir("Kunden/" + str(IDEnde)):
		if int(KundenID) < int(x) or int(KundenID) == int(x):
			KundenID = int(x) + 10
	Debug("KundenID : " + str(KundenID))
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
	NeueKundenDatei = "Kunden/" + str(KundenIDEnde) + "/" + str(KundenID)
	BlueSave("Name", NeuerName, NeueKundenDatei)
	BlueSave("Tel", NeueTel, NeueKundenDatei)
	BlueSave("Adr", NeueAdr, NeueKundenDatei)
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
