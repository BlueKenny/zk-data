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
				if not BurkardtCode == 0: # IM STOCK
					print("Im Stock")
					BurkardtCodeChar = BurkardtCode[-3] + BurkardtCode[-2] + BurkardtCode[-1]
					if not os.path.exists("stock/" + str(BurkardtCodeChar)): os.mkdir("stock/" + str(BurkardtCodeChar))
					stockdatei = "stock/" + str(BurkardtCodeChar) + "/" + str(BurkardtCode)
					
					#	Name
					BlueSave("Name", Name, stockdatei)
					#	Preise
					BlueSave("PreisVKH", PreisVKH, stockdatei)
					BlueSave("PreisVK", PreisVK, stockdatei)
					BlueSave("PreisEK", PreisEK, stockdatei)
					#	Anzahl
					stockAnzahl = BlueLoad("Anzahl", stockdatei)
					if stockAnzahl == None: stockAnzahl = 0
					BlueSave("Anzahl", int(stockAnzahl) + int(Anzahl), stockdatei)
					# idem keybinder ist dran ;)
				else: # Artikel existiert noch nicht
					print("Artikel existiert noch nicht")
					#keybinder klickt auf fenster GSInfo
					#keybinder klickt auf Artikel
					#keybinder druckt F6 und copiert BurkardtCode in den Cache
					#BurkardtCode = cache
					# BurkardtCodeChar = BurkardtCode[-3] + BurkardtCode[-2] + BurkardtCode[-1]
					# if not os.path.exists("stock/" + str(BurkardtCodeChar)): os.mkdir("stock/" + str(BurkardtCodeChar))
					# stockdatei = "stock/" + str(BurkardtCodeChar) + "/" + str(BurkardtCode)
					#	Name
					# BlueSave("Name", Name, stockdatei)
					# keybinder wahlt Name und gibt ihn ein
					#	Preise
					#BlueSave("PreisVKH", PreisVKH, stockdatei)
					#BlueSave("PreisVK", PreisVK, stockdatei)
					#BlueSave("PreisEK", PreisEK, stockdatei)
					# keybinder wahlt VKH und gibt ein
					# keybinder wahlt VK und gibt ein
					# keybinder wahlt EK und gibt ein
					#	Anzahl
					#stockAnzahl = Anzahl
					#BlueSave("Anzahl", int(stockAnzahl), stockdatei)
					# keybinder speichert
					# keybinder geht auf etiket
					# keybinder gibt anzahl ein und druckt
					# keybinder wahlt mouvement
					# keybinder fugt BurkardtCode ein
					# keybinder gibt anzahl ein
				

StartIt()
