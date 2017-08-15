#!/usr/bin/env python3.6
from appJar import gui  
from debug import Debug
from send import *
import os
import sys
import datetime
import subprocess

ID = sys.argv[1]
Debug("ID : " + str(ID))

appInfo = gui("Kunden", "800x600") 

data = GetKunde(ID)
Name = data.split("&KK&")[0]
Tel = data.split("&KK&")[1]
Adr = data.split("&KK&")[2]
Notiz = data.split("&KK&")[3]

text = "ID"; appInfo.addLabel(text, ID)
text = "Name"; appInfo.addLabelEntry(text); appInfo.setEntry(text, Name)
text = "Tel"; appInfo.addLabelEntry(text); appInfo.setEntry(text, Tel)
text = "Adr"; appInfo.addLabelEntry(text); appInfo.setEntry(text, Adr)
text = "Notiz"; appInfo.addTextArea(text);
appInfo.setTextArea(text, Notiz.replace("&+&", "\n"))

def FuncSave(btn):
	Debug("FuncSave")
	appInfo.infoBox("Kunde speichern", "Kunde wurde gespeichert")
	text = "Name"; BlueSave(text, appInfo.getEntry(text), datei); Debug("Speichere |" + appInfo.getEntry(text) + "| in |" + datei + "|")
	text = "Tel"; BlueSave(text, appInfo.getEntry(text), datei); Debug("Speichere |" + appInfo.getEntry(text) + "| in |" + datei + "|")
	text = "Adr"; BlueSave(text, appInfo.getEntry(text), datei); Debug("Speichere |" + appInfo.getEntry(text) + "| in |" + datei + "|")
	text = "Notiz"; BlueSave(text, appInfo.getTextArea(text).replace("\n", "&+&"), datei); Debug("Speichere |" + appInfo.getTextArea(text) + "| in |" + datei + "|")
	
def FuncDelete(btn):	
	Debug("FuncDelete")
	while appInfo.yesNoBox("Löschen?", "Kunde wirklich löschen?"):
		Debug("Lösche Kunde " + ID)
		os.remove(datei)
		appInfo.stop()
		break

def FuncNeuArbeitskarte(btn):	
	Debug("FuncNeuArbeitskarte")
	IDEnde = randint(int(IDMin), int(IDMax))
	Debug("IDEnde : " + str(IDEnde))
	AbID = int(IDEnde)
	for x in os.listdir("Arbeitskarten/" + str(IDEnde)):
		if int(AbID) < int(x) or int(AbID) == int(x):
			AbID = int(x) + 10
	Debug("AbID : " + str(AbID))
	dateiA = "Arbeitskarten/" + str(IDEnde) + "/" + str(AbID)
	BlueSave("KundeID", ID, dateiA)
	print(datetime.datetime.today().strftime("%d/%m/%Y"))
	BlueSave("Datum", datetime.datetime.today().strftime("%d/%m/%Y"), dateiA)
	os.system("./KundeArbeitskarte.py " + str(AbID))
	GESTARTET=False
	FuncSearchArbeitskarten("")

def FuncNeuRechnung(btn):	
	Debug("FuncNeuRechnung")
	IDEnde = randint(int(IDMin), int(IDMax))
	Debug("IDEnde : " + str(IDEnde))
	AbID = int(IDEnde)
	for x in os.listdir("Rechnungen/" + str(IDEnde)):
		if int(AbID) < int(x) or int(AbID) == int(x):
			AbID = int(x) + 10
	Debug("AbID : " + str(AbID))
	dateiR = "Rechnungen/" + str(IDEnde) + "/" + str(AbID)
	BlueSave("KundeID", ID, dateiR)
	print(datetime.datetime.today().strftime("%d/%m/%Y"))
	BlueSave("Datum", datetime.datetime.today().strftime("%d/%m/%Y"), dateiR)
	os.system("./KundeRechnung.py " + str(AbID))
	GESTARTET=False
	FuncSearchRechnugen("")
		
def FuncSearchArbeitskarten(btn):
	global AnzahlArbeitskarten
	Debug("FuncSearchArbeitskarten")
	BlueSave("Work", "Arbeitskarten", TMP)
	BlueSave("ID", ID, TMP)
	if os.path.exists(TMP + "-Arbeitskarten"):
		for eachF in os.listdir(TMP + "-Arbeitskarten/"):
			os.remove(TMP + "-Arbeitskarten/" + eachF);
	else: os.mkdir(TMP + "-Arbeitskarten")
	for z in os.listdir("Arbeitskarten/"):
		open(TMP + str(z) + "GO", "w").write(" ")
		subprocess.Popen(["./SucheProcess.py " + str(z)], shell = True)
	while True:
		Fertig = True
		for z in os.listdir("Arbeitskarten/"):
			if os.path.exists(TMP + str(z) + "GO"):
				Fertig = False
			else:
				if os.path.exists(TMP + str(z)):
					for ArbeitskarteID in open(TMP + str(z), "r").readlines():
						ArbeitskarteID = ArbeitskarteID.rstrip()	
						ArbeitskarteDatei =  "Arbeitskarten/" + ArbeitskarteID[-1] + "/" + ArbeitskarteID
						open(TMP + "-Arbeitskarten/" + ArbeitskarteID, "w").write(ArbeitskarteID)
					os.remove(TMP + str(z))
		if Fertig: break
	if btn == "Arbeitskarten":
		OpenArbeitskarte = appInfo.openBox(title="Arbeitskarten", dirName=TMP + "-Arbeitskarten/", fileTypes=None, asFile=False)
		OpenArbeitskarte = open(OpenArbeitskarte, "r").read()
		os.system("./KundeArbeitskarte.py " + OpenArbeitskarte + " &")
	AnzahlArbeitskarten = len(os.listdir(TMP + "-Arbeitskarten/"))
	appInfo.setButton("Arbeitskarten", str(AnzahlArbeitskarten) + " Arbeitskarten")
	print("FERTIG")

def FuncSearchRechnungen(btn):
	global AnzahlRechnungen
	Debug("FuncSearchRechnungen")
	BlueSave("Work", "Rechnungen", TMP)
	BlueSave("ID", ID, TMP)
	if os.path.exists(TMP + "-Rechnungen"):
		for eachF in os.listdir(TMP + "-Rechnungen/"):
			os.remove(TMP + "-Rechnungen/" + eachF);
	else: os.mkdir(TMP + "-Rechnungen")
	for z in os.listdir("Rechnungen/"):
		open(TMP + str(z) + "GO", "w").write(" ")
		subprocess.Popen(["./SucheProcess.py " + str(z)], shell = True)
	while True:
		Fertig = True
		for z in os.listdir("Rechnungen/"):
			if os.path.exists(TMP + str(z) + "GO"):
				Fertig = False
			else:
				if os.path.exists(TMP + str(z)):
					for RechnungID in open(TMP + str(z), "r").readlines():
						RechnungID = RechnungID.rstrip()	
						RechnungDatei =  "Rechnungen/" + RechnungID[-1] + "/" + RechnungID
						open(TMP + "-Rechnungen/" + RechnungID, "w").write(RechnungID)
					os.remove(TMP + str(z))
		if Fertig: break
	if btn == "Rechnungen":
		OpenRechnung = appInfo.openBox(title="Rechnungen", dirName=TMP + "-Rechnungen/", fileTypes=None, asFile=False)
		OpenRechnung = open(OpenRechnung, "r").read()
		os.system("./KundeRechnung.py " + OpenRechnung + " &")
	AnzahlRechnungen = len(os.listdir(TMP + "-Rechnungen/"))
	appInfo.setButton("Rechnungen", str(AnzahlRechnungen) + " Rechnungen")
	print("FERTIG")

def FuncPrint(btn):
	Debug("FuncPrint")
	KundeDaten = open("Vorlage/Kunde", "r").read()
	KundeDaten = KundeDaten.replace("OOOTel", BlueLoad("Tel", datei))
	KundeDaten = KundeDaten.replace("OOOName", ID + "  " + BlueLoad("Name", datei))
	KundeDaten = KundeDaten.replace("OOOAdresse", BlueLoad("Adr", datei))
	open(TMP + "-PRINT", "w").write(KundeDaten)
	os.system("gedit " + TMP + "-PRINT")

appInfo.addButton("Neue Arbeitskarte", FuncNeuArbeitskarte)
appInfo.addButton("Neue Rechnung", FuncNeuRechnung)
appInfo.addButton("Arbeitskarten", FuncSearchArbeitskarten)
FuncSearchArbeitskarten("")
appInfo.setButton("Arbeitskarten", str(AnzahlArbeitskarten) + " Arbeitskarten")
appInfo.addButton("Rechnungen", FuncSearchRechnungen)
FuncSearchRechnungen("")
appInfo.setButton("Rechnungen", str(AnzahlRechnungen) + " Rechnungen")
appInfo.bindKey("<Escape>", FuncSave)
appInfo.bindKey("<Delete>", FuncDelete)
appInfo.addButton("Speichern", FuncSave)
appInfo.addButton("Drucken", FuncPrint)
appInfo.go()
