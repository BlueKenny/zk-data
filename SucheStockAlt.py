#!/usr/bin/env python
from appJar import gui
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
from debug import *
import os
import subprocess
from random import randint
# Lieferant
EntryList=["Bcode", "Artikel", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Stock Suche", "500x600") 

Lieferanten=[]
#Lieferanten=["stihl", "gm", "kockelmann", "eurogarden", "kramp" ,"roxauto", "hartje", "now company","agu", "cosmic sports", "hilaire van der haeghe", "unimet", "kraftwerk", "ratioparts", "velz", "wolf-zondervan", "zeg", "innotec", "bergtoys", "dong feng", "knegt", "van droogenbroeck", "motor snelco", "van dyck"]

# MAKE CACHE
print("Make Cache")
CacheArtikel=[]
CacheName=[]
CacheOrt=[]
CachePreisEK=[]
CachePreisVKH=[]
CachePreisVK=[]
CacheAnzahl=[]
CacheLieferant=[]
CacheBarcode=[]

for x in range(000000, 999999):
	Prozent=x/999999*100
	#print("MAKE CACHE : " + str(Prozent) + " %")
	CacheArtikel.insert(x, "")
	CacheName.insert(x, "")
	CacheOrt.insert(x, "")
	CachePreisEK.insert(x, "")
	CachePreisVKH.insert(x, "")
	CachePreisVK.insert(x, "")
	CacheAnzahl.insert(x, "")
	CacheLieferant.insert(x, "")
	CacheBarcode.insert(x, "")

# LOAD CACHE
print("Load Cache")
TotalArt=0
for dirs in os.listdir("Stock/"):
	Debug("LOAD " + str(dirs))
	for files in os.listdir("Stock/" + str(dirs) + "/"):
		TotalArt = TotalArt + 1
		x = "Stock/" + str(dirs) + "/" + str(files)
		files = int(files)
		CacheArtikel[files] = BlueLoad("Artikel", x)
		CacheName[files] = BlueLoad("Name", x)
		CacheOrt[files] = BlueLoad("Ort", x)
		CachePreisEK[files] = BlueLoad("PreisEK", x)
		CachePreisVKH[files] = BlueLoad("PreisVKH", x)
		CachePreisVK[files] = BlueLoad("PreisVK", x)
		CacheAnzahl[files] = BlueLoad("Anzahl", x)
		CacheLieferant[files] = BlueLoad("Lieferant", x)
		CacheBarcode[files] = BlueLoad("Barcode", x)
		if not BlueLoad("Lieferant", x) in Lieferanten:
			Lieferanten.append(BlueLoad("Lieferant", x))

def FuncSave(btn):
	Debug("FuncSave")
	BcodeSuche = appSuche.getEntry("Bcode")
	pfad = "Stock/" + BcodeSuche[-3] + BcodeSuche[-2] + BcodeSuche[-1] + "/"
	Debug("pfad : " + str(pfad))
	BlueMkDir(pfad)
	datei = pfad + BcodeSuche
	BlueSave("Barcode", appSuche.getEntry("Barcode").lower(), datei)
	BlueSave("Artikel", appSuche.getEntry("Artikel").lower(), datei)
	BlueSave("Name", appSuche.getEntry("Name").lower(), datei)
	BlueSave("Ort", appSuche.getEntry("Ort").lower(), datei)
	
	BlueSave("PreisEK", appSuche.getEntry("PreisEK").lower(), datei)
	BlueSave("PreisVKH", appSuche.getEntry("PreisVKH").lower(), datei)
	BlueSave("PreisVK", appSuche.getEntry("PreisVK").lower(), datei)
	BlueSave("Anzahl", appSuche.getEntry("Anzahl").lower(), datei)
	BlueSave("Lieferant", appSuche.getOptionBox("Lieferant"), datei)

	BcodeSuche = int(BcodeSuche)
	CacheBarcode[BcodeSuche] = appSuche.getEntry("Barcode").lower()
	CacheArtikel[BcodeSuche] = appSuche.getEntry("Artikel").lower()
	CacheName[BcodeSuche] = appSuche.getEntry("Name").lower()
	CacheOrt[BcodeSuche] = appSuche.getEntry("Ort").lower()
	CachePreisEK[BcodeSuche] = appSuche.getEntry("PreisEK").lower()
	CachePreisVKH[BcodeSuche] = appSuche.getEntry("PreisVKH").lower()
	CachePreisVK[BcodeSuche] = appSuche.getEntry("PreisVK").lower()
	CacheAnzahl[BcodeSuche] = appSuche.getEntry("Anzahl").lower()
	CacheLieferant[BcodeSuche] = appSuche.getOptionBox("Lieferant")

def FuncSuche3(btn):
	Debug("FuncSuche3")

	appSuche.setEntry("Bcode", "")
	appSuche.setEntry("Barcode", "")
	appSuche.setOptionBox("Lieferant", "")
	appSuche.setEntry("Name", "")
	appSuche.setEntry("Ort", "")
	appSuche.setEntry("PreisEK", "")
	appSuche.setEntry("PreisVKH", "")
	appSuche.setEntry("PreisVK", "")
	appSuche.setEntry("Anzahl", "")

	ArtikelSuche = appSuche.getEntry("Artikel")
	Debug("ArtikelSuche : " + str(ArtikelSuche))
	BcodeSuche = CacheArtikel.index(str(ArtikelSuche))

	appSuche.setEntry("Bcode", BcodeSuche)
	appSuche.setEntry("Barcode", CacheBarcode[BcodeSuche])
	appSuche.setOptionBox("Lieferant", CacheLieferant[BcodeSuche])
	appSuche.setEntry("Name", CacheName[BcodeSuche])
	appSuche.setEntry("Ort", CacheOrt[BcodeSuche])
	appSuche.setEntry("PreisEK", CachePreisEK[BcodeSuche])
	appSuche.setEntry("PreisVKH", CachePreisVKH[BcodeSuche])
	appSuche.setEntry("PreisVK", CachePreisVK[BcodeSuche])
	appSuche.setEntry("Anzahl", CacheAnzahl[BcodeSuche])

def FuncSuche2(btn):
	global datei
	Debug("FuncSuche2")

	appSuche.setEntry("Bcode", "")
	appSuche.setEntry("Artikel", "")
	appSuche.setOptionBox("Lieferant", "")
	appSuche.setEntry("Name", "")
	appSuche.setEntry("Ort", "")
	appSuche.setEntry("PreisEK", "")
	appSuche.setEntry("PreisVKH", "")
	appSuche.setEntry("PreisVK", "")
	appSuche.setEntry("Anzahl", "")

	BarcodeSuche = int(appSuche.getEntry("Barcode"))
	Debug("BarcodeSuche : " + str(BarcodeSuche))

	BcodeSuche  = CacheBarcode.index(str(BarcodeSuche))
	appSuche.setEntry("Bcode", BcodeSuche)

	appSuche.setEntry("Artikel", CacheArtikel[BcodeSuche])
	appSuche.setOptionBox("Lieferant", CacheLieferant[BcodeSuche])
	appSuche.setEntry("Name", CacheName[BcodeSuche])
	appSuche.setEntry("Ort", CacheOrt[BcodeSuche])
	appSuche.setEntry("PreisEK", CachePreisEK[BcodeSuche])
	appSuche.setEntry("PreisVKH", CachePreisVKH[BcodeSuche])
	appSuche.setEntry("PreisVK", CachePreisVK[BcodeSuche])
	appSuche.setEntry("Anzahl", CacheAnzahl[BcodeSuche])
	
def FuncSuche(btn):
	global datei
	Debug("FuncSuche")

	appSuche.setEntry("Barcode", "")
	appSuche.setEntry("Artikel", "")
	appSuche.setOptionBox("Lieferant", "")
	appSuche.setEntry("Name", "")
	appSuche.setEntry("Ort", "")
	appSuche.setEntry("PreisEK", "")
	appSuche.setEntry("PreisVKH", "")
	appSuche.setEntry("PreisVK", "")
	appSuche.setEntry("Anzahl", "")

	BcodeSuche = int(appSuche.getEntry("Bcode"))
	Debug("BcodeSuche : " + str(BcodeSuche))

	appSuche.setEntry("Barcode", CacheBarcode[BcodeSuche])
	appSuche.setEntry("Artikel", CacheArtikel[BcodeSuche])
	appSuche.setOptionBox("Lieferant", CacheLieferant[BcodeSuche])
	appSuche.setEntry("Name", CacheName[BcodeSuche])
	appSuche.setEntry("Ort", CacheOrt[BcodeSuche])
	appSuche.setEntry("PreisEK", CachePreisEK[BcodeSuche])
	appSuche.setEntry("PreisVKH", CachePreisVKH[BcodeSuche])
	appSuche.setEntry("PreisVK", CachePreisVK[BcodeSuche])
	appSuche.setEntry("Anzahl", CacheAnzahl[BcodeSuche])

def Best(btn):
        AnzahlZUBestellen = appSuche.numberBox("Bestellen", "Wie viele sollen bestelt werden?")
        BCODEzuBEstellen = appSuche.getEntry("Bcode")
        BlueSave(str(BCODEzuBEstellen), str(AnzahlZUBestellen), "BestStock")
        appSuche.infoBox("In Bestellung", "Dein artikel \n" + str(appSuche.getEntry("Name") + "\nist in bestellung"))

def ChangeStock(btn):
        Anz = int(appSuche.getEntry("Anzahl"))
        if btn == "Artikel PLUS": Anz = Anz + 1
        else: Anz = Anz - 1
        appSuche.setEntry("Anzahl", Anz)
        BlueSave(appSuche.getEntry("Bcode"), appSuche.getEntry("Anzahl"), "ChStock")
        FuncSave("")

appSuche.addLabelEntry("Bcode")
appSuche.addButton("Suche", FuncSuche)
appSuche.addLabelEntry("Barcode")
appSuche.addButton("Suche2", FuncSuche2)
appSuche.addLabelEntry("Artikel")
appSuche.addButton("Suche3", FuncSuche3)

appSuche.addLabelOptionBox("Lieferant", Lieferanten)

#appSuche.addLabelEntry("Lieferant")
appSuche.addLabelEntry("Name")
appSuche.addLabelEntry("Ort")
appSuche.addLabelEntry("PreisEK")
appSuche.addLabelEntry("PreisVKH")
appSuche.addLabelEntry("PreisVK")
appSuche.addLabelEntry("Anzahl")

appSuche.addLabel("Total Artkel", str(TotalArt) + " Artikel im Stock")


appSuche.addButton("Artikel MINUS", ChangeStock)
appSuche.addButton("Artikel PLUS", ChangeStock)


appSuche.addButton("Bitte Bestellen", Best)


#appSuche.bindKey("<Return>", FuncSuche)
appSuche.bindKey("<Escape>", FuncSave)
appSuche.go()
