#!/usr/bin/env python3.6
from appJar import gui  
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import RoundUp
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

datei = "Rechnungen/" + ID[-1] + "/" + ID

appRechnung = gui("Rechnung", "800x600") 

text = "ID"; appRechnung.addLabel(text, ID)

#	datum
appRechnung.addLabel("datum", "Datum der Rechnung : ")
datum = BlueLoad("Datum", datei)
text = "Datum"; appRechnung.addLabel(text, datum)
#appRechnung.addDatePicker("datum")
#appRechnung.setDatePicker("datum", date=str(datum))

def FuncSetMachine(btn):
	global Machine
	Machine = appRechnung.openBox(title="Machine", dirName="Machinen/", fileTypes=None, asFile=False)
	Debug("Machine : " + str(Machine))
	appRechnung.setButton("Machine", open(Machine, "r").read().rstrip())

def FuncSetUnterschrift(btn):
	global Unterschrift
	Unterschrift = appRechnung.openBox(title="Unterschrift", dirName="Unterschrift/", fileTypes=None, asFile=False)
	Debug("Unterschrift : " + str(Unterschrift))
	appRechnung.setButton("Unterschrift", open(Unterschrift, "r").read().rstrip())

dateiKunde = "Kunden/" + BlueLoad("KundeID", datei)[-1] + "/" + BlueLoad("KundeID", datei)
text = "KundeID"; appRechnung.addLabel(text, text + ": " + BlueLoad(text, datei))
text = "Name"; appRechnung.addLabel(text, text + ": " + BlueLoad(text, dateiKunde))
text = "Tel"; appRechnung.addLabel(text, text + ": " + BlueLoad(text, dateiKunde))
text = "Adr"; appRechnung.addLabel(text, text + ": " + BlueLoad(text, dateiKunde))

Machine = BlueLoad("Machine", datei)
text = "Machine"; appRechnung.addNamedButton(text, text, FuncSetMachine)
if Machine == None or Machine == "None": FuncSetMachine("")
else: appRechnung.setButton("Machine", open(Machine, "r").read().rstrip())


Unterschrift = BlueLoad("Unterschrift", datei)
text = "Unterschrift"; appRechnung.addNamedButton(text, text, FuncSetUnterschrift)
if Unterschrift == None or Unterschrift == "None": FuncSetUnterschrift("")
else: appRechnung.setButton("Unterschrift", open(Unterschrift, "r").read().rstrip())

#Auszuführende Arbeiten : OOOFDaten
text = "FDaten"; appRechnung.addListBox(text)
appRechnung.clearListBox(text)
try:
	FDaten = BlueLoad("FDaten", datei)
	for Linien in FDaten.split("&+&"):
		Debug("Rechnung Linie : " + str(Linien))
		appRechnung.addListItem("FDaten", Linien)
except:
	FDaten = ""


def FuncSave(btn):
	Debug("FuncSave")
	appRechnung.infoBox("Rechnung speichern", "Rechnung wurde gespeichert")
	text = "Machine"; BlueSave(text, Machine, datei)
	text = "Unterschrift"; BlueSave(text, Unterschrift, datei)

	text = "FDaten"; ArtikelLinien = appRechnung.getAllListItems(text)
	addThisText = ""
	for eachArtikelLinie in ArtikelLinien:
		Debug("eachArtikelLinie : " + eachArtikelLinie)
		if not addThisText == "":addThisText = addThisText + "&+&" + eachArtikelLinie
		else: addThisText = eachArtikelLinie
	Debug("addThisText : " + addThisText)
	BlueSave(text, addThisText, datei)

def FuncPrint(btn):
	global FDaten
	FuncSave("")
	Debug("FuncPrint")
	appRechnung.infoBox("Rechnung drucken", "Rechnung wird gedruckt")
	KarteDaten = open("Vorlage/Rechnung").read()
	KarteDaten = KarteDaten.replace("OOODatum", datum)
	KarteDaten = KarteDaten.replace("OOOTel", BlueLoad("Tel", dateiKunde))
	KarteDaten = KarteDaten.replace("OOOMachine", open(Machine, "r").read().rstrip())
	KarteDaten = KarteDaten.replace("OOOName", BlueLoad("KundeID", datei) + "  " + BlueLoad("Name", dateiKunde))
	KarteDaten = KarteDaten.replace("OOOAdresse", BlueLoad("Adr", dateiKunde))
	KarteDaten = KarteDaten.replace("OOOID", ID)	

	text = "FDaten"; ArtikelLinien = appRechnung.getAllListItems(text)
	addThisText = "\n"
	for eachArtikelLinie in ArtikelLinien:
		Debug("eachArtikelLinie : " + eachArtikelLinie)
		xAnzahl=eachArtikelLinie.split(" | ")[0]
		xArtikel=eachArtikelLinie.split(" | ")[1]
		xPreis=eachArtikelLinie.split(" | ")[2]
		Line = xAnzahl + "x	" + xArtikel + "	" + xPreis
		if not addThisText == "":addThisText = addThisText + "\n" + Line
		else: addThisText = Line
	Debug("addThisText : " + addThisText)
	KarteDaten = KarteDaten.replace("OOOFDaten", addThisText)

	KarteDaten = KarteDaten.replace("OOOFUnterschrift", open(Unterschrift, "r").read().rstrip())
	open(TMP + "-PRINT", "w").write(KarteDaten)
	os.system("gedit " + TMP + "-PRINT")


def FuncDelete(btn):	
	Debug("FuncDelete")
	while appRechnung.yesNoBox("Löschen?", "Rechnung wirklich löschen?"):
		Debug("Lösche Rechnung " + ID)
		os.remove(datei)
		appRechnung.stop()
		break

def FuncAddLine(btn):
	Debug("FuncAddLine")
	Anzahl = appRechnung.numberBox("Anzahl", "Anzahl")
	Artikel = appRechnung.textBox("Artikel", "Artikel einscannen oder text eingeben")
	try:
		int(Artikel)
		cc = "Zahl"
	except:
		cc = "Text"

	if len(Artikel) == 6 and cc == "Zahl": # Bcode
		Debug("Bcode")

	if len(Artikel) == 13 and cc == "Zahl": # Barcode
		Debug("Barcode")

	if not len(Artikel) == 6 and not len(Artikel) == 13 : # Text
		Debug("Text")

	Preis = appRechnung.numberBox("Preis", "Preis")

	appRechnung.addListItem("FDaten", str(Anzahl) + " | " + str(Artikel) + " | " + str(Preis))

def FuncRemoveLine(btn):
	Debug("FuncRemoveLine")
	SelectedLinie = appRechnung.getListItems("FDaten")
	print(SelectedLinie)
	appRechnung.removeListItem("FDaten", SelectedLinie)
	

appRechnung.bindKey("<Escape>", FuncSave)
appRechnung.bindKey("<Print>", FuncPrint)
appRechnung.bindKey("<Delete>", FuncDelete)
appRechnung.addButton("Linie +", FuncAddLine)
appRechnung.addButton("Linie -", FuncRemoveLine)
appRechnung.addButton("Speichern", FuncSave)
appRechnung.addButton("Drucken", FuncPrint)
appRechnung.go()
