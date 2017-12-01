#!/usr/bin/env python3
from libs.appjar0061 import gui  
from BlueFunc import *
from debug import Debug
import os
import subprocess
from random import randint
import send
import shutil

if not Date() == BlueLoad("LastUpdate", "DATA"):
	try: os.system("./Updater.pyw")
	except: os.system("Updater.pyw")

EntryList=["Kundennummer", "Vorname",  "Nachname", "Tel", "Adresse", "Ort"]
EntryList2=["Vorname",  "Nachname", "Tel", "Adresse", "Ort"]
appSuche = gui("Kunden Suche", "800x600") 

IDToChange = 0

appSuche.addMeter("status"); appSuche.setMeterFill("status", "blue")
appSuche.setMeter("status", 100, text="")

def tbFuncSv(btn):
	global IDToChange
	Debug("tbFuncSv")
	for a in EntryList2:
		print(appChange.getEntry(a))
		send.KundeSetInfo(IDToChange, a, appChange.getEntry(a))
	appChange.stop()
	Delete("")
	appSuche.setEntry("Name", IDToChange)
	Suche("")

def tbFunc(btn):
	global IDToChange
	global appChange
	Debug("btn : " + btn)

	if btn == "NEU":
		Number = send.NeueKundenID()

		IDToChange = Number
		appChange = gui("Kunde Change", "800x600")
		appChange.addLabel("Kundennummer", str(IDToChange))
		GetThis = ""
		for a in EntryList2:
			GetThis = GetThis + "(zkz)" + str(a)
		Data = send.KundeGetInfo(GetThis, str(IDToChange)).split(" | ")
		for x in range(0, len(EntryList2)):
			appChange.addLabelEntry(EntryList2[x]); appChange.setEntry(EntryList2[x], Data[x+1], callFunction=False)
		
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()
		
	if btn == "ÄNDERN":
		IDToChange = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
		appChange = gui("Kunde Change", "800x600")
		appChange.addLabel("Kundennummer", str(IDToChange))
		GetThis = ""
		for a in EntryList2:
			GetThis = GetThis + "(zkz)" + str(a)
		Data = send.KundeGetInfo(GetThis, str(IDToChange)).split(" | ")
		print(Data)
		for x in range(0, len(EntryList2)):
			appChange.addLabelEntry(EntryList2[x]); appChange.setEntry(EntryList2[x], Data[x+1], callFunction=False)
		
		appChange.addLabel("info", "F5 = Speichern")
		appChange.bindKey("<F5>", tbFuncSv)
		appChange.go()

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addTickOptionBox("Anzeigen", EntryList2)
try:
	for eachAnzeigenOption in BlueLoad("Anzeigen-Kunden", "DATA").split("/"):
		appSuche.setOptionBox("Anzeigen", eachAnzeigenOption, value=True, callFunction=True)
except: print("Anzeigen nicht gefunden")

appSuche.addLabelEntry("Name")
appSuche.addLabelEntry("Tel")
appSuche.addLabelEntry("Adresse/Ort")
appSuche.addListBox("Suche")

def Delete(btn):
	Debug("Delete")
	appSuche.setEntry("Name", "")
	appSuche.setEntry("Tel", "")
	appSuche.setEntry("Adresse/Ort", "")

def Suche(btn):
	Debug("Suche")
	appSuche.setMeter("status", 0, text="Suche wird gestartet")
	
	AntwortList=send.SendeSucheKunde(appSuche.getEntry("Name").lower(), appSuche.getEntry("Tel"), appSuche.getEntry("Adresse/Ort").lower())
	appSuche.setMeter("status", 10, text="Warte auf daten")
	appSuche.clearListBox("Suche")

	Schritt = (100-10)/(len(AntwortList.split("<K>"))-1); print("Schritt : " + str(Schritt))
	for IDs in AntwortList.split("<K>"):
		if not IDs == "":
			appSuche.setMeter("status", appSuche.getMeter("status")[0]*100 + Schritt, text="Sammle Daten")
			print("status : " + str(appSuche.getMeter("status")[0] + Schritt))
			Linie = str(IDs).rstrip()
			GetThis = ""
			for a in EntryList2:
				if appSuche.getOptionBox("Anzeigen")[a] and not IDs.rstrip() == "":
					GetThis = GetThis + "(zkz)" + str(a)
			Linie = send.KundeGetInfo(GetThis, IDs)

			appSuche.addListItem("Suche", Linie)
	
	appSuche.setLabel("infoAnzahl", str(send.GetKundenZahl()) + " Kunden im System")
	appSuche.setMeter("status", 100, text="")

def SaveIt():
	Debug("SaveIt")
	for each in EntryList2:
		if appSuche.getOptionBox("Anzeigen")[each]:
			try: AnzeigenListe = AnzeigenListe + "/" + each
			except: AnzeigenListe = each
	try:
		print(AnzeigenListe)
		BlueSave("Anzeigen-Kunden", AnzeigenListe, "DATA")
	except:
		print("AnzeigenListe ist leer")
		BlueSave("Anzeigen-Kunden", "Vorname/Nachname/Tel/Adresse/Ort", "DATA")
	return True

appSuche.setFocus("Name")
appSuche.addLabel("info", "Enter = Suche \nDelete = Clear")
appSuche.addLabel("infoAnzahl", str(send.GetKundenZahl()) + " Kunden im System")
appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<Delete>", Delete)
appSuche.setStopFunction(SaveIt)
appSuche.go()
