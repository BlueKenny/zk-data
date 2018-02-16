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
appSuche = gui("Search Stock", "800x800")
#appSuche.setSticky("news")
#appSuche.setExpand("both")
#appSuche.setFont(12)
appSuche.setBg("#3399ff")
#appSuche.setIcon("DATA/stock.jpg")

IDToChange = 0
AlteSuche = ""

AutoCacheSlowDown = False

def BtnStockGraph(btn):
    ID = appSuche.getListBox("Suche")[0].split(" | ")[0]
    print("ID " + str(ID))

    if not "P" in ID:
        if platform.system() == "Linux": COMMAND = "./ArtGraph.py "
        if platform.system() == "Windows": COMMAND = "ArtGraph.py "
        os.system(COMMAND + str(ID))

def BtnPrintBarcode(btn):
    ID = str(appSuche.getListItems("Suche")[0].split(" | ")[0]).rstrip()
    print("ID " + ID)

    if not "P" in ID:
        Data = GetArt(ID)
        Anzahl = appSuche.numberBox("Drucken", "Welche Anzahl soll gedruckt werden?")
        for a in range(0, Anzahl):
            PrintBarcode("", Data.identification, Data.barcode, Data.name_de, Data.preisvk)

def BtnPrintOrt(btn):
    ID = str(appSuche.getListItems("Suche")[0].split(" | ")[0]).rstrip()
    print("ID " + ID)

    if not "P" in ID:
        Data = GetArt(ID)
        PrintLocation(Data.ort)

def ArtikelAnzeigen():
    global AlteSuche
    print("ArtikelAnzeigen")
    ID = str(appSuche.getListBox("Suche")[0].split(" | ")[0]).rstrip()
    print("ID:" + ID)
    if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
    if platform.system() == "Windows":  COMMAND = "ChangeStock.pyw"
    application = os.popen(COMMAND + " " + ID).readlines()
    if not str(BlueLoad("LastID", "DATA/DATA")) == "None":
        appSuche.setEntry("Suche", BlueLoad("LastID", "DATA/DATA"))
        AlteSuche = ""

def tbFunc(btn):
    global IDToChange
    global appChange
    Debug("btn : " + btn)

    if btn == "NEU":
        object = GetID()
        if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
        if platform.system() == "Windows": COMMAND = "ChangeStock.pyw"
        COMMAND = COMMAND + " " + str(object.identification)
        application = os.popen(COMMAND).readlines()
    if btn == "F1 -": StockChange("<F1>")
    if btn == "F2 +": StockChange("<F2>")
    if btn == "F11 Ort": BtnPrintOrt("")
    if btn == "F12 Barcode": BtnPrintBarcode("")
    Delete("")
    appSuche.setEntry("Suche", BlueLoad("LastID", "DATA/DATA"))


tools = ["NEU", "", "F1 -", "F2 +", " ", "F11 Ort", "F12 Barcode"]
appSuche.addToolbar(tools, tbFunc, findIcon=False)


appSuche.addDualMeter("progress", 0, 0)
appSuche.setMeterFill("progress", ["red", "green"])
appSuche.setMeter("progress", [0, 0])

appSuche.addLabelEntry("Suche", 1, 0, 1, 0)
#appSuche.addLabelEntry("Ort", 1, 1, 1, 0)
#appSuche.addLabelEntry("Lieferant", 1, 2, 1, 0)

#GridSuche = appSuche.addGrid("Suche", [["Identification", "Artikel", "Lieferant", "Name", "Ort", "Preis", "Anzahl"]],
#                             action=ArtikelAnzeigen,
#                             actionHeading="Informationen",
#                             actionButton="Anzeigen",
#                             showMenu=False)
#appSuche.setGridHeight("Suche", 500)

ListBoxSuche = appSuche.addListBox("Suche", [], 2, 0, 3, 2)
appSuche.setListBoxHeight("Suche", 30)
ListBoxSuche.bind("<Double-1>", lambda *args: ArtikelAnzeigen())# if List Item double click then change


def Delete(btn):
    Debug("Delete")
    appSuche.setEntry("Suche", "")
    #appSuche.setEntry("Ort", "")
    #appSuche.setEntry("Lieferant", "")
    appSuche.setFocus("Suche")


def Suche():
    appSuche.thread(SucheProcess)
    appSuche.after(500, Suche)

def SucheProcess():
    global AutoCacheSlowDown
    global AlteSuche
    Suche = appSuche.getEntry("Suche")
    if not AlteSuche == Suche:
        Debug("Suche")

        AlteSuche = Suche

        #appSuche.deleteAllGridRows("Suche")
        #appSuche.addGridRows("Suche", [["Identification", "Artikel", "Lieferant", "Name", "Ort", "Preis", "Anzahl"]])
        appSuche.clearListBox("Suche")
        AutoCacheSlowDown = True

        #appSuche.setMeter("status", 0, text="Suche wird gestartet")

        EndString = ""
        for character in Suche:
            if character.isalpha() or character.isdigit():
                EndString = EndString + str(character)
        Suche = EndString.upper()
        appSuche.setEntry("Suche", Suche, callFunction=False)

        Ort = ""
        #Ort = appSuche.getEntry("Ort")
        #EndString = ""
        #for character in Ort:
        #    if character.isalpha() or character.isdigit():
        #        EndString = EndString + str(character)
        #    Ort = EndString.upper()
        #appSuche.setEntry("Ort", Ort, callFunction=False)

        Lieferant = ""
        #Lieferant = appSuche.getEntry("Lieferant")
        #EndString = ""
        #for character in Lieferant:
        #    if character.isalpha() or character.isdigit():
        #        EndString = EndString + str(character)
        #    Lieferant = EndString.upper()
        #appSuche.setEntry("Lieferant", Lieferant, callFunction=False)

        if Suche == "":
            NichtSuchen = True
        else:
            NichtSuchen = False

        if not NichtSuchen:
            #AntwortListStock=SendeSucheStock(Suche, Ort, Lieferant).split("<K>")
            #print("AntwortListStock " + str(AntwortListStock))

            AntwortDict=SearchArt({"suche":Suche, "ort":Ort, "lieferant":Lieferant})

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
                    #appSuche.addGridRows("Suche", [[str(ID),
                    #                               str(Art.artikel),
                    #                               str(Art.lieferant),
                    #                               str(Art.name),
                    #                               str(Art.ort),
                    #                               str(Art.preisvk),
                    #                               str(Art.anzahl)]])
                    Linie = str(ID)
                    Linie = Linie + " | " + str(Art.artikel)
                    Linie = Linie + " | " + str(Art.lieferant)
                    Linie = Linie + " | " + str(Art.name_de)
                    Linie = Linie + " | " + str(Art.ort)
                    Linie = Linie + " | " + str(Art.preisvk)
                    Linie = Linie + " | " + str(Art.anzahl)
                    appSuche.addListItem("Suche", Linie)
                    appSuche.setListItemBg("Suche", Linie, "#ffffff")

            appSuche.selectListItemAtPos("Suche", 0, callFunction=False)
    

def StockChange(btn):
    global AlteSuche
    Debug("StockChange")
    try: IDToChange = appSuche.getListBox("Suche")[0].split(" | ")[0].rstrip()
    except: appSuche.errorBox("Fehler", "Bitte wählen sie zuerst einen Artikel aus")
    if not "P" in IDToChange:
        if btn == "<F1>": # MINUS
            Anzahl = appSuche.numberBox("Entfernen", "Wie viele wolen sie ENTFERNEN ?")
            if Anzahl == None:
                appSuche.errorBox("Fehler", "Abgebrochen")
            else:
                try:
                    object = AddArt(IDToChange, "-" + str(int(Anzahl)))
                    Debug(IDToChange)
                    if not object == {}:
                        if not object.anzahl < 0:
                            appSuche.infoBox("Gespeichert", "Anzahl wurde geändert")
                            appSuche.setEntry("Suche", IDToChange)
                    else:
                        appSuche.infoBox("Fehler", "Anzahl wurde nicht geändert")
                except: appSuche.infoBox("Fehler", "Fehler")
        if btn == "<F2>": # PLUS
            Anzahl = appSuche.numberBox("Hinzufügen", "Wie viele wollen sie HINZUFUGEN ?")
            if Anzahl == None:
                appSuche.errorBox("Fehler", "Abgebrochen")
            else:
                try:
                    object = AddArt(IDToChange, int(Anzahl))
                    Debug(IDToChange)
                    if not object == {}:
                        if not object.anzahl < 0:
                            appSuche.infoBox("Gespeichert", "Anzahl wurde geändert")
                            appSuche.setEntry("Suche", IDToChange)
                    else:
                        appSuche.infoBox("Fehler", "Anzahl wurde nicht geändert")
                except: appSuche.infoBox("Fehler", "Fehler")
    AlteSuche = ""

def AutoMakeCacheProcess():
    global AutoCacheSlowDown
    BewegungLocalIndex = GetBewegungIndexLocal()
    BewegungServerIndex = GetBewegungIndex()
    if BewegungLocalIndex < BewegungServerIndex:
        GetBewegung(BewegungLocalIndex)
        if AutoCacheSlowDown:
            appSuche.after(10000, AutoMakeCache)
            AutoCacheSlowDown = False
        else:
            appSuche.after(10, AutoMakeCache)
    else:
        appSuche.after(60000, AutoMakeCache)

def AutoMakeCache():
    appSuche.thread(AutoMakeCacheProcess)

def AutoProgressBarProcess():
    print("\nProcess")
    Dict = GetBewegungTagLocal()
    Ausgaben = 0.0
    Einnahmen = 0.0
    for ID, object in Dict.items():
        #print("ID:" + str(ID))
        Anzahl = float(object.end) - float(object.start)

        if Anzahl < 0.0:
            Sum = object.preisvkh * Anzahl
            Einnahmen = Einnahmen - Sum
        else:
            Sum = object.preisek * Anzahl
            Ausgaben = Ausgaben + Sum
    while True:
        if Einnahmen > 100 or Ausgaben > 100:
            Einnahmen = Einnahmen / 2
            Ausgaben = Ausgaben / 2
        else: break
    print("Ausgaben: " + str(Ausgaben) + "  Einnahmen: " + str(Einnahmen) + "\n")
    appSuche.setMeter("progress", [Ausgaben, Einnahmen])
    appSuche.after(5000, AutoProgressBar)

def AutoProgressBar():
    appSuche.thread(AutoProgressBarProcess)


appSuche.setFocus("Suche")

#appSuche.setEntryChangeFunction("Suche", Suche)
#appSuche.setEntryChangeFunction("Ort", Suche)
#appSuche.setEntryChangeFunction("Lieferant", Suche)

appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F4>", BtnStockGraph)
appSuche.bindKey("<F11>", BtnPrintOrt)
appSuche.bindKey("<F12>", BtnPrintBarcode)
appSuche.bindKey("<Delete>", Delete)

appSuche.after(1000, Suche)
appSuche.after(1000, AutoMakeCache)
appSuche.after(1000, AutoProgressBar)

appSuche.go()
