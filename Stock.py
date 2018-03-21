#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send

class Main:    
    def __init__(self):
        print("init")
        #self.busy(False)
        self.ScanForSearch()
    
    def ScanForSearch(self):
        #self.busy(True)

        if True:
            libs.send.SendBild("/home/phablet/Pictures/scan.jpg")
            os.remove("/home/phablet/Pictures/scan.jpg")
            #libs.send.GetBarcode("/home/phablet/Pictures/scan.jpg")
            barcode = "ok"
            print("barcode: " + str(barcode))
        if False:
            barcode = "nichts"
            os.system("test_vibrator")

        os.system("test_vibrator")
        #pyotherside.send("antwortScanForSearch", barcode)

        #self.busy(False)
    
    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
    def busy2(self, status):
        status = bool(status)
        print("busy2 = " + str(status))
        pyotherside.send("busy2", status)
        
    def GetArt(self, ID):
        print("antwortGetArt")
        self.busy2(True)
        Dict = libs.send.GetArt(str(ID))
        if len(Dict) == 0:
            os.system("test_vibrator")
        del Dict["identification"]

        Antwort = []
        for text, var in sorted(Dict.items()):
            print("text:" + str(text) + " var:" + str(var))
            Antwort.append({"name": str(text), "var" : str(var)})
        pyotherside.send("antwortGetArt", Antwort)
        self.busy2(False)
        
    
    def SearchArt(self, suche):
        self.busy(True)
        if not suche == "":
            Antwort = []
            IDList = libs.send.SearchArt({"suche": suche, "ort": "", "lieferant": ""})
            for ID in IDList:
                self.busy(True)
                Dict = libs.send.GetArt(str(ID))
                Antwort.append(Dict)
                self.busy(False)
            pyotherside.send("antwortSearchArt", Antwort) 
            if len(IDList) == 0:
                os.system("test_vibrator")
        self.busy(False)

    def isPhone(self):
        if os.path.exists("/home/phablet"):
            handy = True
            pyotherside.send("ifPhone", handy)
        else: handy = False
        print("isPhone: " + str(handy))
        self.busy(False)
    
    def isPhone2(self):
        if os.path.exists("/home/phablet"):
            handy = True
            pyotherside.send("ifPhone2", handy)
        else: handy = False
        print("isPhone2: " + str(handy))
        self.busy2(False)
        
main = Main()

