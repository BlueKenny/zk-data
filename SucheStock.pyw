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
appSuche.setBg("#ffffff")
#appSuche.setIcon("DATA/stock.jpg")

IDToChange = 0
ServerStockIsOn = True
ServerPreiscorschlagIsOn = True

try: AutoCacheID = int(BlueLoad("AutoCacheID", "DATA/DATA"))
except: AutoCacheID = 1
AutoCacheSlowDown = False

#NEWS
#NEWS_INDEX = BlueLoad("NEWS_INDEX", "DATA/DATA")
#if NEWS_INDEX == None: NEWS_INDEX = 40
#NEWS_INDEX = int(NEWS_INDEX)
#with codecs.open("news.csv", "r", "utf-8") as csvfile:
#    reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
#    for eachLine in reader:
#       if not "INDEX" in eachLine and NEWS_INDEX < int(eachLine[0]):
#            print(eachLine)
#            NEWS_INDEX = int(eachLine[0])
#            appSuche.infoBox("Update " + eachLine[0], eachLine[1] + "\n\n" + eachLine[3], parent=None)
#BlueSave("NEWS_INDEX", NEWS_INDEX, "DATA/DATA")

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
    print("ArtikelAnzeigen")
    ID = str(appSuche.getListBox("Suche")[0].split(" | ")[0]).rstrip()
    print("ID:" + ID)
    if platform.system() == "Linux": COMMAND = "./ChangeStock.pyw"
    if platform.system() == "Windows":  COMMAND = "ChangeStock.pyw"
    application = os.popen(COMMAND + " " + ID).readlines()
    appSuche.setEntry("Suche", BlueLoad("LastID", "DATA/DATA"))
    Suche()

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

appSuche.addLabelEntry("Suche", 0, 0, 1, 0)
appSuche.addLabelEntry("Ort", 0, 1, 1, 0)
appSuche.addLabelEntry("Lieferant", 0, 2, 1, 0)
#GridSuche = appSuche.addGrid("Suche", [["Identification", "Artikel", "Lieferant", "Name", "Ort", "Preis", "Anzahl"]],
#                             action=ArtikelAnzeigen,
#                             actionHeading="Informationen",
#                             actionButton="Anzeigen",
#                             showMenu=False)
#appSuche.setGridHeight("Suche", 500)
ListBoxSuche = appSuche.addListBox("Suche", [], 1, 0, 3, 8)
ListBoxSuche.bind("<Double-1>", lambda *args: ArtikelAnzeigen())# if List Item double click then change

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
    #appSuche.deleteAllGridRows("Suche")
    #appSuche.addGridRows("Suche", [["Identification", "Artikel", "Lieferant", "Name", "Ort", "Preis", "Anzahl"]])
    appSuche.clearListBox("Suche")
    AutoCacheSlowDown = True

    #appSuche.setMeter("status", 0, text="Suche wird gestartet")

    Suche = appSuche.getEntry("Suche")
    EndString = ""
    for character in Suche:
        if character.isalpha() or character.isdigit():
            EndString = EndString + str(character)
    Suche = EndString.upper()
    appSuche.setEntry("Suche", Suche, callFunction=False)

    Ort = appSuche.getEntry("Ort")
    EndString = ""
    for character in Ort:
        if character.isalpha() or character.isdigit():
            EndString = EndString + str(character)
        Ort = EndString.upper()
    appSuche.setEntry("Ort", Ort, callFunction=False)

    Lieferant = appSuche.getEntry("Lieferant")
    EndString = ""
    for character in Lieferant:
        if character.isalpha() or character.isdigit():
            EndString = EndString + str(character)
        Lieferant = EndString.upper()
    appSuche.setEntry("Lieferant", Lieferant, callFunction=False)

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
    BlueSave("LastID", IDToChange, "DATA/DATA")

def AutoMakeCacheProcess():
    global AutoCacheID
    global AutoCacheSlowDown

    if not AutoCacheID == GetBewegungIndex():
        GetBewegung(AutoCacheID)
        AutoCacheID = AutoCacheID + 1
        if AutoCacheSlowDown:
            appSuche.after(10000, AutoMakeCache)
            AutoCacheSlowDown = False
        else:
            appSuche.after(10, AutoMakeCache)
        BlueSave("AutoCacheID", AutoCacheID, "DATA/DATA")
    else:
        appSuche.after(60000, AutoMakeCache)

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
#appSuche.addLabel("Keys", "Entfernen = Alle fehler leeren\n" +
#                  "F1 = Artikel entfernen\n" +
#                  "F2 = Artikel hinzufügen\n" +
#                  "F11 = Ort drucken\n" +
#                  "F12 = Drucken",
#                  15, 0, 3, 3)

#appSuche.addLabel("infoAnzahlStock",  "")
#appSuche.addLabel("infoAnzahlPreisvorschlag",  "")

#appSuche.bindKey("<Return>", Suche)
appSuche.setEntryChangeFunction("Suche", Suche)
appSuche.setEntryChangeFunction("Ort", Suche)
appSuche.setEntryChangeFunction("Lieferant", Suche)

appSuche.bindKey("<F1>", StockChange)
appSuche.bindKey("<F2>", StockChange)
appSuche.bindKey("<F4>", BtnStockGraph)
appSuche.bindKey("<F11>", BtnPrintOrt)
appSuche.bindKey("<F12>", BtnPrintBarcode)
appSuche.bindKey("<Delete>", Delete)

appSuche.after(1000, AutoMakeCache)
#appSuche.after(500, CheckAnzahl)
appSuche.go()
