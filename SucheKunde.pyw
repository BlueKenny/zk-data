#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.appjar0830 import gui
from libs.BlueFunc import *
from libs.debug import Debug
import os
import platform
from libs.send import *
import sys

if len(sys.argv) < 0:
	ID = int(sys.argv[1])
else:
	ID = 0

EntryList=["Name", "Tel", "Tel2", "Adresse", "Ort", "Fax", "Email"]
appSuche = gui("Kunden Suche", "800x600")
appSuche.setBg("#ffffff")


appSuche.addMeter("status"); appSuche.setMeterFill("status", "blue")
appSuche.setMeter("status", 100, text="")

def tbFuncSv(btn):
	global IDToChange
	Debug("tbFuncSv")
	for a in EntryList2:
		print(appChange.getEntry(a))
		KundeSetInfo(IDToChange, a, appChange.getEntry(a))
	appChange.stop()
	Delete("")
	appSuche.setEntry("Name", IDToChange)
	Suche("")

def tbFunc(btn):
    global IDToChange
    global appChange
    Debug("tbFunc : " + btn)

    if btn == "NEW":
        if platform.system() == "Linux": COMMAND = "./ChangeKunde.pyw"
        if platform.system() == "Windows": COMMAND = "ChangeKunde.pyw"
        application = os.popen(COMMAND).readlines()
        Suche(BlueLoad("LastID", "DATA/DATA"))

    if btn == "CHANGE":
        ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
        if platform.system() == "Linux": COMMAND = "./ChangeKunde.pyw"
        if platform.system() == "Windows": COMMAND = "ChangeKunde.pyw"
        application = os.popen(COMMAND + " " + ID).readlines()
        Suche(BlueLoad("LastID", "DATA/DATA"))

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=True)

appSuche.addLabelEntry("Name")
appSuche.addLabelEntry("Tel")
appSuche.addLabelEntry("Adresse/Ort")
appSuche.addListBox("Suche")

def KundeSetzen(btn):
	Debug("KundeSetzen")
	IDKunden = appSuche.getListItems("Suche")[0].split(" | ")[0].rstrip()
	BlueSave("KundenID", IDKunden, "TMP")
	appSuche.stop()

def Delete(btn):
	Debug("Delete")
	appSuche.setEntry("Name", "")
	appSuche.setEntry("Tel", "")
	appSuche.setEntry("Adresse/Ort", "")

def Suche(btn):
    Debug("Suche")
    appSuche.setMeter("status", 0, text="Suche wird gestartet")
    Name = appSuche.getEntry("Name")
    Tel = appSuche.getEntry("Tel")
    Ort = appSuche.getEntry("Adresse/Ort")

    if not Name == "" and not Tel == "" and not Ort == "":
        AntwortList=SendeSucheKunde(appSuche.getEntry("Name").lower(), appSuche.getEntry("Tel"), appSuche.getEntry("Adresse/Ort").lower())
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
                Linie = KundeGetInfo(GetThis, IDs)

                appSuche.addListItem("Suche", Linie)

    appSuche.setLabel("infoAnzahl", str(GetKundenZahl()) + " Kunden im System")
    appSuche.setMeter("status", 100, text="")


appSuche.setFocus("Name")
appSuche.addLabel("info", "Enter = Suche \nDelete = Clear")
appSuche.addLabel("infoAnzahl", str(GetKundenZahl()) + " Kunden im System")

appSuche.bindKey("<Return>", Suche)
appSuche.bindKey("<Delete>", Delete)
appSuche.go()
