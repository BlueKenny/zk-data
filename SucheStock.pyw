#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
if not os.path.exists("DATA/NOUPDATE"):
    print("Update")
    os.system("git pull")
else:
    print("No Update")

from libs.appjar0900 import gui
from libs.BlueFunc import *
from libs.debug import Debug
from libs.send import *
from libs.barcode import *
import csv

EntryList=["Barcode", "Artikel", "Artikel2", "Artikel3", "Lieferant", "Name", "Ort", "PreisEK", "PreisVKH", "PreisVK", "Anzahl"]
appSuche = gui("Search Stock", "800x650")
appSuche.setBg("#ffffff")

IDToChange = 0
ServerStockIsOn = True
ServerPreiscorschlagIsOn = True

AutoCacheID = 100000
AutoCacheSlowDown = False
#appSuche.addMeter("status"); appSuche.setMeterFill("status", "blue")
#appSuche.setMeter("status", 100, text="")

#NEWS
NEWS_INDEX = BlueLoad("NEWS_INDEX", "DATA/DATA")
if NEWS_INDEX == None: NEWS_INDEX = 20
NEWS_INDEX = int(NEWS_INDEX)
with codecs.open("news.csv", "r", "utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
    for eachLine in reader:
        if not "INDEX" in eachLine and NEWS_INDEX < int(eachLine[0]):
            print(eachLine)
            NEWS_INDEX = int(eachLine[0])
            appSuche.infoBox("Update " + eachLine[0], eachLine[1] + "\n\n" + eachLine[3], parent=None)
BlueSave("NEWS_INDEX", NEWS_INDEX, "DATA/DATA")

def BtnStockGraph(btn):
    ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
    print("ID " + str(ID))

    if not "P" in ID:
        if platform.system() == "Linux": COMMAND = "./ArtGraph.py "
        if platform.system() == "Windows": COMMAND = "ArtGraph.py "
        os.system(COMMAND + str(ID))

def BtnPrintBarcode(btn):
    ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
    print("ID " + str(ID))

    if not "P" in ID:
        GetData = StockGetArtInfo(["Barcode", "Name", "PreisVK"], ID).split(" | ")
        print("GetData " + str(GetData))

        Anzahl = appSuche.numberBox("Drucken", "Welche Anzahl soll gedruckt werden?")
        for a in range(0, Anzahl):
            PrintBarcode("", GetData[0], GetData[1], GetData[2], GetData[3])

def BtnPrintOrt(btn):
    ID = appSuche.getListItems("Suche")[0].split(" | ")[0]
    print("ID " + str(ID))

    if not "P" in ID:
        PrintLocation(StockGetArtInfo(["Ort"], ID).split(" | ")[1])


appSuche.addLabelEntry("Suche")
appSuche.addLabelEntry("Ort")
appSuche.addLabelEntry("Lieferant")
ListBoxSuche = appSuche.addListBox("Suche")
ListBoxSuche.bind("<Double-1>", lambda *args: tbFunc("ÄNDERN"))# if List Item double click then change

def tbFunc(btn):
    global IDToChange
    global appChange
    Debug("btn : " + btn)

    if btn == "NEU":
        if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
        if platform.system() == "Windows": COMMAND = "ChangeStock.pyw"
        application = os.popen(COMMAND).readlines()
        Suche(BlueLoad("LastID", "DATA/DATA"))

    if btn == "ÄNDERN":
        ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
        if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
        if platform.system() == "Windows":  COMMAND = "ChangeStock.pyw"
        application = os.popen(COMMAND + " " + ID).readlines()
        Suche(BlueLoad("LastID", "DATA/DATA"))

tools = ["NEU", "ÄNDERN"]
appSuche.addToolbar(tools, tbFunc, findIcon=False)

def Delete(btn):
    Debug("Delete")
    appSuche.setEntry("Suche", "")
    appSuche.setEntry("Ort", "")
    appSuche.setEntry("Lieferant", "")
    appSuche.setFocus("Suche")


def Suche():
    appSuche.thread(SucheProcess)

def SucheProcess():
    global AutoCacheSlowDown
    Debug("Suche")
    appSuche.clearListBox("Suche")
    AutoCacheSlowDown = True

    #appSuche.setMeter("status", 0, text="Suche wird gestartet")

    Suche = appSuche.getEntry("Suche").replace(" ", "").upper()
    Ort = appSuche.getEntry("Ort").upper()
    Lieferant = appSuche.getEntry("Lieferant").upper()

    if Suche == "":
        NichtSuchen = True
    else:
        NichtSuchen = False

    if not NichtSuchen:
        #AntwortListStock=SendeSucheStock(Suche, Ort, Lieferant).split("<K>")
        #print("AntwortListStock " + str(AntwortListStock))

        if ServerStockIsOn:
            AntwortDict=SearchArt({"suche":Suche, "ort":Ort, "lieferant":Lieferant})
            #print("AntwortDict " + str(AntwortDict))
        else: AntwortList=[]

        #if ServerPreiscorschlagIsOn:
        #    for ID, Time in SuchePreisvorschlag(Suche, Lieferant).items():
        #        AntwortDict[ID]=str(Time)
        #AntwortListPreisvorschlag=SendeSuchePreisvorschlag(Suche, Lieferant).split("<K>")
        #print("AntwortListPreisvorschlag " + str(AntwortListPreisvorschlag))

        print("AntwortDict: " + str(AntwortDict))
        for ID, Time in AntwortDict.items():
            if not ID == "":
                print("ID: " + str(ID))
                print(" Time: " + str(Time))

                ArtLocal = GetArtLocal(ID)
                if str(ArtLocal.lastchange) == str(Time):
                    Art = ArtLocal
                    print(" GetArtLocal")
                else:
                    Art = GetArt(ID)
                    print(" GetArtServer")

                Linie = str(ID)
                Linie = Linie + " | " + str(Art.artikel)
                Linie = Linie + " | " + str(Art.lieferant)
                Linie = Linie + " | " + str(Art.name)
                Linie = Linie + " | " + str(Art.ort)
                Linie = Linie + " | " + str(Art.preisvk)
                Linie = Linie + " | " + str(Art.anzahl)
                appSuche.addListItem("Suche", Linie)
                appSuche.setListItemBg("Suche", Linie, "#ffffff")

    #    AntwortList=[]
    #    for each in AntwortListStock:
    #        if not each == "": AntwortList.append(each)
    #    for each in AntwortListPreisvorschlag:
    #        if not each == "": AntwortList.append(each)

    #    appSuche.setMeter("status", 10, text="Warte auf daten")
    #    appSuche.clearListBox("Suche")

    #    if btn == "first":
    #        AntwortList = [AntwortList[0]]
    #        Schritt = (100-10)/(1); print("Schritt " + str(Schritt))
    #    else:
    #        Schritt = (100-10)/(len(AntwortList)-1); print("Schritt " + str(Schritt))

    #    print("AntwortList " + str(AntwortList))
    #    for IDs in AntwortList:
    #        Debug("Get Info for ID " + str(IDs))
    #        if not IDs == "" and not IDs == "0"and not IDs == None and not IDs == "None" and not IDs == "P0":
    #            appSuche.setMeter("status", appSuche.getMeter("status")[0] * 100 + Schritt, text="Lade Daten")
    #            print(" " + str(appSuche.getMeter("status")[0] + Schritt))
    #            Linie = str(IDs).rstrip()
    #            if "P" in IDs:
    #                Linie = "P" + PreisvorschlagGetArtInfo(["Artikel", "LieferantMitDatum", "Name", "PreisVK"], IDs)
    #            else:
    #                Linie = StockGetArtInfo(["Artikel", "Lieferant", "Name", "Ort", "PreisVK", "Anzahl"], IDs)

    #            appSuche.addListItem("Suche", Linie)
    #            if "P" in IDs:
    #                appSuche.setListItemBg("Suche", Linie, "#FFF68F")
    #            else:
    #                appSuche.setListItemBg("Suche", Linie, "#ffffff")
    #    appSuche.selectListItemAtPos("Suche", 0, callFunction=False)


    #StockAnzahl = int(GetStockZahl())
    #appSuche.setLabel("infoAnzahlStock",  str(GetStockZahl()) + " Artikel zu verfügung")
    #if StockAnzahl == 0:
    #    appSuche.setLabelFg("infoAnzahlStock", "red")
    #else:
    #    appSuche.setLabelFg("infoAnzahlStock", "green")

    #PreisvorschlagAnzahl = int(GetStockPreisvorschlagAnzahl())
    #appSuche.setLabel("infoAnzahlPreisvorschlag",  str(GetStockPreisvorschlagAnzahl()) + " Preisvorschläge")
    #if PreisvorschlagAnzahl == 0:
    #    appSuche.setLabelFg("infoAnzahlPreisvorschlag", "red")
    #else:
    #    appSuche.setLabelFg("infoAnzahlPreisvorschlag", "green")

    #appSuche.setMeter("status", 100, text="")

def StockChange(btn):
    Debug("StockChange")
    try: IDToChange = appSuche.getListBox("Suche")[0].split(" | ")[0].rstrip()
    except: appSuche.errorBox("Fehler", "Bitte wählen sie zuerst einen Artikel aus")
    if not "P" in IDToChange:
        Name = "[ " + StockGetArtInfo(["Name"], str(IDToChange)) + " ]"
        if btn == "<F1>": # MINUS
            Anzahl = appSuche.numberBox("Entfernen", "Wie viele wolen sie ENTFERNEN ?")
            if Anzahl == None:
                appSuche.errorBox("Fehler", "Abgebrochen")
            else:
                try:
                    SendeChangeAnzahl(IDToChange, "-" + str(int(Anzahl)))
                    Debug(IDToChange)
                    appSuche.infoBox("Gespeichert", "Anzahl wurde geändert")
                    appSuche.setEntry("Suche", IDToChange)
                    #Suche("first")
                except: appSuche.infoBox("Fehler", "Fehler")
        if btn == "<F2>": # PLUS
            Anzahl = appSuche.numberBox("Hinzufügen", "Wie viele wollen sie HINZUFUGEN ?")
            if Anzahl == None:
                appSuche.errorBox("Fehler", "Abgebrochen")
            else:
                try:
                    SendeChangeAnzahl(IDToChange, int(Anzahl))
                    Debug(IDToChange)
                    appSuche.infoBox("Gespeichert", "Anzahl wurde geändert")
                    appSuche.setEntry("Suche", IDToChange)
                    #Suche("first")
                except: appSuche.infoBox("Fehler", "Fehler")

def AutoMakeCacheProcess():
    global AutoCacheID
    global AutoCacheSlowDown

    GetArt(AutoCacheID)
    AutoCacheID = AutoCacheID + 1

    if not AutoCacheID == 1000000:
        if AutoCacheSlowDown:
            appSuche.after(10000, AutoMakeCache)
            AutoCacheSlowDown = False
        else:
            appSuche.after(100, AutoMakeCache)

def AutoMakeCache():
    appSuche.thread(AutoMakeCacheProcess)

def CheckAnzahl():
    global ServerStockIsOn
    global ServerPreiscorschlagIsOn

    StockAnzahl = int(GetStockZahl())
    PreisvorschlagAnzahl = int(GetStockPreisvorschlagAnzahl())
    appSuche.setLabel("infoAnzahlStock", str(StockAnzahl) + " Artikel zu verfügung")
    appSuche.setLabel("infoAnzahlPreisvorschlag", str(PreisvorschlagAnzahl) + " Preisvorschläge")

    if StockAnzahl == 0:
        appSuche.setLabelFg("infoAnzahlStock", "red")
        ServerStockIsOn = False
    else:
        appSuche.setLabelFg("infoAnzahlStock", "green")
        ServerStockIsOn = True

    if PreisvorschlagAnzahl == 0:
        appSuche.setLabelFg("infoAnzahlPreisvorschlag", "red")
        ServerPreiscorschlagIsOn = False
    else:
        appSuche.setLabelFg("infoAnzahlPreisvorschlag", "green")
        ServerPreiscorschlagIsOn = True
    if not ServerStockIsOn or not ServerPreiscorschlagIsOn:
        appSuche.after(1000, CheckAnzahl)
    else:
        appSuche.after(10000, CheckAnzahl)


appSuche.setFocus("Suche")
#appSuche.addLabel("KeyEnter", "Enter = Suchen")
appSuche.addLabel("KeyDelete", "Entfernen = Alle fehler leeren")
appSuche.addLabel("space0", "")
appSuche.addLabel("KeyF1", "F1 = Artikel entfernen")
appSuche.addLabel("KeyF2", "F2 = Artikel hinzufügen")
appSuche.addLabel("KeyF11", "F11 = Ort drucken")
appSuche.addLabel("KeyF12", "F12 = Drucken")
appSuche.addLabel("space1", "")

appSuche.addLabel("infoAnzahlStock",  "")
appSuche.addLabel("infoAnzahlPreisvorschlag",  "")

appSuche.addLabel("space2", "")

#appSuche.bindKey("<Return>", Suche)
appSuche.setEntryChangeFunction("Suche", Suche)
appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F4>", BtnStockGraph)
appSuche.bindKey("<F11>", BtnPrintOrt)
appSuche.bindKey("<F12>", BtnPrintBarcode)
appSuche.bindKey("<Delete>", Delete)
appSuche.after(10000, AutoMakeCache)

#appSuche.after(500, CheckAnzahl)
appSuche.go()
