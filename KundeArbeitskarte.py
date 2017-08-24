#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import Debug
import os
import sys
import subprocess
from random import randint

# PC ID setzen, damit mehrere PCs gleichzeitig dieses program benutzen können
pcid = os.getenv("HOSTNAME")
TMP = "tmp/" + pcid

ID = sys.argv[1]
Debug("ID : " + str(ID))

datei = "Arbeitskarten/" + ID[-1] + "/" + ID

appArbeitskarte = gui("Arbeitskarte", "800x600") 

text = "ID"; appArbeitskarte.addLabel(text, ID)

#	datum
appArbeitskarte.addLabel("datum", "Datum der Arbeitskarte : ")
datum = BlueLoad("Datum", datei)
text = "Datum"; appArbeitskarte.addLabel(text, datum)
#appArbeitskarte.addDatePicker("datum")
#appArbeitskarte.setDatePicker("datum", date=str(datum))

def FuncSetMachine(btn):
	global Machine
	Machine = appArbeitskarte.openBox(title="Machine", dirName="Machinen/", fileTypes=None, asFile=False)
	Debug("Machine : " + str(Machine))
	appArbeitskarte.setButton("Machine", open(Machine, "r").read().rstrip())

def FuncSetUnterschrift(btn):
	global Unterschrift
	Unterschrift = appArbeitskarte.openBox(title="Unterschrift", dirName="Unterschrift/", fileTypes=None, asFile=False)
	Debug("Unterschrift : " + str(Unterschrift))
	appArbeitskarte.setButton("Unterschrift", open(Unterschrift, "r").read().rstrip())

appArbeitskarte.addLabel("fdatum", "Fertigstellen bis : ");
fdatum = BlueLoad("FDatum", datei)
if fdatum == None:
	fdatum = datum
	#fdatumjahr = appArbeitskarte.numberBox("Datum", "Fertigstellen bis : Jahr")
	#fdatummonat = appArbeitskarte.textBox("Datum", "Fertigstellen bis : Monat")
	#fdatumtag = appArbeitskarte.textBox("Datum", "Fertigstellen bis : Tag")
	#fdatum = fdatumjahr + "-" + fdatummonat + "-" + fdatumtag
text = "FDatum"; appArbeitskarte.addLabelEntry(text); appArbeitskarte.setEntry(text, fdatum)

dateiKunde = "Kunden/" + BlueLoad("KundeID", datei)[-1] + "/" + BlueLoad("KundeID", datei)
text = "KundeID"; appArbeitskarte.addLabel(text, text + ": " + BlueLoad(text, datei))
text = "Name"; appArbeitskarte.addLabel(text, text + ": " + BlueLoad(text, dateiKunde))
text = "Tel"; appArbeitskarte.addLabel(text, text + ": " + BlueLoad(text, dateiKunde))
text = "Adr"; appArbeitskarte.addLabel(text, text + ": " + BlueLoad(text, dateiKunde))

Machine = BlueLoad("Machine", datei)
text = "Machine"; appArbeitskarte.addNamedButton(text, text, FuncSetMachine)
if Machine == None or Machine == "None": FuncSetMachine("")
else: appArbeitskarte.setButton("Machine", open(Machine, "r").read().rstrip())


Unterschrift = BlueLoad("Unterschrift", datei)
text = "Unterschrift"; appArbeitskarte.addNamedButton(text, text, FuncSetUnterschrift)
if Unterschrift == None or Unterschrift == "None": FuncSetUnterschrift("")
else: appArbeitskarte.setButton("Unterschrift", open(Unterschrift, "r").read().rstrip())

#Auszuführende Arbeiten : OOOFDaten
text = "FDaten"; appArbeitskarte.addTextArea(text)
try: FDaten = BlueLoad("FDaten", datei).replace("&+&", "\n")
except: FDaten = ""
appArbeitskarte.setTextArea(text, FDaten)

def FuncSave(btn):
	Debug("FuncSave")
	appArbeitskarte.infoBox("Arbeitskarte speichern", "Arbeitskarte wurde gespeichert")
	text = "FDatum"; BlueSave(text, appArbeitskarte.getEntry(text), datei)
	text = "Machine"; BlueSave(text, Machine, datei)
	text = "Unterschrift"; BlueSave(text, Unterschrift, datei)
	text = "FDaten"; BlueSave(text, appArbeitskarte.getTextArea(text).replace("\n", "&+&"), datei)

def FuncPrint(btn):
	global FDaten
	FuncSave("")
	Debug("FuncPrint")
	appArbeitskarte.infoBox("Arbeitskarte drucken", "Arbeitskarte wird gedruckt")
	KarteDaten = open("Vorlage/Arbeitskarte").read()
	KarteDaten = KarteDaten.replace("OOODatum", datum)
	KarteDaten = KarteDaten.replace("OOOTel", BlueLoad("Tel", dateiKunde))
	KarteDaten = KarteDaten.replace("OOOMachine", open(Machine, "r").read().rstrip())
	KarteDaten = KarteDaten.replace("OOOName", BlueLoad("KundeID", datei) + "  " + BlueLoad("Name", dateiKunde))
	KarteDaten = KarteDaten.replace("OOOAdresse", BlueLoad("Adr", dateiKunde))
	KarteDaten = KarteDaten.replace("OOOFDatum", fdatum)	
	KarteDaten = KarteDaten.replace("OOOID", ID)
	FDaten = appArbeitskarte.getTextArea("FDaten")
	t1= "\n"; t2="\n                + "
	FDaten = FDaten.replace(t1,t2)
	KarteDaten = KarteDaten.replace("OOOFDaten", "\n" + t2 + FDaten)
	KarteDaten = KarteDaten.replace("OOOFUnterschrift", open(Unterschrift, "r").read().rstrip())
	open(TMP + "-PRINT", "w").write(KarteDaten)
	os.system("gedit " + TMP + "-PRINT")


def FuncDelete(btn):	
	Debug("FuncDelete")
	while appArbeitskarte.yesNoBox("Löschen?", "Arbeitskarte wirklich löschen?"):
		Debug("Lösche Arbeitskarte " + ID)
		os.remove(datei)
		appArbeitskarte.stop()
		break

appArbeitskarte.bindKey("<Escape>", FuncSave)
appArbeitskarte.bindKey("<Print>", FuncPrint)
appArbeitskarte.bindKey("<Delete>", FuncDelete)
appArbeitskarte.addButton("Speichern", FuncSave)
appArbeitskarte.addButton("Drucken", FuncPrint)
appArbeitskarte.go()
