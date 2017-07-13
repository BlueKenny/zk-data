#!/usr/bin/env python
from appJar import gui  
import os
import sys
import pickle
import time
import datetime
from BlueVar import *
from BlueFunc import *
from Data import *



def GetKundenInfo(KundeID):
	print("GetKundenInfo")
	app = gui("Kunden", "600x400")
	app.setLocation(0, 200)

	for ESTRING in AlleDaten:
		app.addLabelEntry(ESTRING)
		app.setEntryDefault(ESTRING, ESTRING)

	for DW in AlleDaten:
		app.setEntry(DW, BlueLoad(DW, "Kunden/" + str(KundeID)))
		app.setEntryDefault(DW, DW)
			
	def Arbeitskarte(btn):
		print("Arbeitskarte")
		ArbeitskarteDaten = open("VorlageArbeitskarte", "r").read()
		
		#	OOOKartenID
		KartenID = 0
		while True:
			if not os.path.exists("Arbeitskarten/" + str(KartenID) + ".txt"): break
			else: KartenID = KartenID + 1
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOKartenID", str(KartenID))

		#	OOODatum
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOODatum", time.strftime("%d/%m/%Y	%H:%M"))
		
		#	OOOKundeID
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOKundeID", str(KundeID))

		#	OOOName
		#	OOOTel
		#	OOOAdresse
		for XA in {"Name", "Tel", "Adresse"}:
			ArbeitskarteDaten = ArbeitskarteDaten.replace("OOO" + XA, str(BlueLoad(XA, "Kunden/" + str(KundeID))))

		#	OOOMachine
		Machine = open(app.openBox(title="Machine", dirName="Machinen", fileTypes=None, asFile=False), "r").readlines()[0]
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOMachine", Machine)

		#	OOOFDatum
		while True:
			FDatum = app.textBox("Fertigstellen bis...", time.strftime("%d/%m/%Y") + " oder " + time.strftime("%d.%m.%Y"))
			try:
				datetime.datetime.strptime(FDatum, '%d/%m/%Y')
				break
			except ValueError:
				try:
					datetime.datetime.strptime(FDatum, '%d.%m.%Y')
					break
				except ValueError:
					app.errorBox("Fertigstellen bis...", "Bitte format beachten :\n" + str(time.strftime("%d/%m/%Y")) + "\n" + str(time.strftime("%d.%m.%Y")))
			
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOFDatum", FDatum)

		#	OOOFDaten
		FDaten = "+" + app.textBox("Arbeit :", "Auszufuehrende Arbeiten : \n + = Neue Zeile")
		FDaten = FDaten.replace("+", "\n\n			+ ")
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOFDaten", FDaten)

		#	OOOFUnterschrift
		FUnterschrift = open(app.openBox(title="Unterschrift", dirName="Unterschrift", fileTypes=None, asFile=False), "r").readlines()[0]
		open("Arbeitskarte.txt", "w").write(ArbeitskarteDaten)
		BlueLen("Arbeits")

		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOFUnterschrift", FUnterschrift)

		#	OOOID
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOID", str(KartenID))
	
		open("Arbeitskarte.txt", "w").write(ArbeitskarteDaten)
		open("Arbeitskarten/" + str(KartenID) + ".txt", "w").write(ArbeitskarteDaten)

		try: os.startfile("Arbeitskarte.txt", "print")
		except: os.system("gedit Arbeitskarte.txt")

	def Rechnung(btn):
		print("Rechnung")
		ArbeitskarteDaten = open("VorlageRechnung", "r").read()

		#SchonGedruckt = app.yesNoBox("Rechnung :", "Liegt die Vorlage schon im drucker?")
		SchonGedruckt = False
		#	OOOKartenID
		KartenID = 0
		while True:
			if not os.path.exists("Rechnung/" + str(KartenID) + ".txt"): break
			else: KartenID = KartenID + 1
		if not SchonGedruckt: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOKartenID", str(KartenID))
		else: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOKartenID", "")

		#	OOODatum
		if not SchonGedruckt: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOODatum", time.strftime("%d/%m/%Y	%H:%M"))
		else: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOODatum", "")
		
		#	OOOKundeID
		if not SchonGedruckt: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOKundeID", str(KundeID))
		else: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOKundeID", "")

		#	OOOName
		#	OOOTel
		#	OOOAdresse
		for XA in {"Name", "Tel", "Adresse"}:
			if not SchonGedruckt: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOO" + XA, str(BlueLoad(XA, "Kunden/" + str(KundeID))))
			else: ArbeitskarteDaten = ArbeitskarteDaten.replace("OOO" + XA, "")

		#	OOOMachine
		if not SchonGedruckt:
			Machine = open(app.openBox(title="Machine", dirName="Machinen", fileTypes=None, asFile=False), "r").readlines()[0]
			ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOMachine", Machine)
		else: 
			ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOMachine", "")

		#	OOOFDaten
		FDaten = ""
		TTotal = 0
		while True:
			Anzahl = app.textBox("Rechnung :", "Anzahl :")  
			Art = app.textBox("Rechnung :", "Artikel :")
			Preis = app.textBox("Rechnung :", "Preis :")
			Total = float(Anzahl) * float(Preis)
			TTotal = TTotal + Total
			Weiter = app.yesNoBox("Weiter Artikel ?", "Weiter Artikel ?")
			FDaten = FDaten + "\n                   " + str(Anzahl) + "x      " + str(Art)
			for x in range(len(Art), 35): FDaten = FDaten + " "
			FDaten = FDaten + str(Preis) + "     " + str(Total)
			print(FDaten)
			if not Weiter: break
		FDaten = FDaten + "\n\n\n\n                          TOTAL = " + str(TTotal) + " Euro"
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOFDaten", FDaten)
		
		#	000FUnterschrift
		if not SchonGedruckt:
			FUnterschrift = open(app.openBox(title="Unterschrift", dirName="Unterschrift", fileTypes=None, asFile=False), "r").readlines()[0]
			ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOFUnterschrift", FUnterschrift)
		else:
			ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOFUnterschrift", "")

		#	OOOID
		ArbeitskarteDaten = ArbeitskarteDaten.replace("OOOID", str(KartenID))

		open("Rechnung.txt", "w").write(ArbeitskarteDaten)
		open("Rechnung/" + str(KartenID) + ".txt", "w").write(ArbeitskarteDaten)

		try: os.startfile("Rechnung.txt", "print")
		except: os.system("gedit Rechnung.txt")
		
	def Speichern(btn):
		print("Speichern")

		for WX in AlleDaten:
			BlueSave(WX, app.getEntry(WX), "Kunden/" + str(KundeID))

		app.stop()	

	app.addButton("Speichern", Speichern)
	app.addButton("Arbeitskarte", Arbeitskarte)
	app.addButton("Rechnung schreiben", Rechnung)
	app.bindKey("<Return>", Speichern)
	app.go()
