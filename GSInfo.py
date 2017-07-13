#!/usr/bin/env python
from keybinder import *
import os
from BlueVar import *

def StartIt():
	for jedenLieferant in os.listdir("barcode/"):
		if os.path.exists(jedenLieferant + "-preis/"):
			print("Start " + jedenLieferant)
			for Artikel in os.listdir(jedenLieferant + "-preis/"):
				print("Artikel : " + Artikel)
				datei = jedenLieferant + "-preis/" + Artikel
				Name = BlueLoad("Name", datei)
				Anzahl = BlueLoad("Anzahl", datei)
				Anzahl = Anzahl.split(".")[0]
				PreisVKH = BlueLoad("PreisVKH", datei)
				PreisVK = BlueLoad("PreisVK", datei)
				PreisEK = BlueLoad("PreisEK", datei)
				BurkardtCode = BlueLoad("BurkardtCode", datei)
				BurkardtCodeChar = BurkardtCode[-3] + BurkardtCode[-2] + BurkardtCode[-1]
				if not os.path.exists("stock/" + str(BurkardtCodeChar)): os.mkdir("stock/" + str(BurkardtCodeChar))
				stockdatei = "stock/" + str(BurkardtCodeChar) + "/" + str(BurkardtCode)
				#	Name
				BlueSave("Name", Name, stockdatei)
				#	Anzahl
				stockAnzahl = BlueLoad("Anzahl", stockdatei)
				if stockAnzahl == None: stockAnzahl = 0
				BlueSave("Anzahl", int(stockAnzahl) + int(Anzahl), stockdatei)
				#	Preise
				BlueSave("PreisVKH", PreisVKH, stockdatei)
				BlueSave("PreisVK", PreisVK, stockdatei)
				BlueSave("PreisEK", PreisEK, stockdatei)

				# if BurkardtCode == 0 dann Hinzufugen

StartIt()
