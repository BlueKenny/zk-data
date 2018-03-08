#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send
import libs.BlueFunc
import libs.RoundUp

LastLieferschein = ""

class Main:    
    def __init__(self):
        global DATA
        global LastLieferschein
        print("init")
            
        self.busy(False)

        DATA = {}
        
        self.GetLieferschein()   

    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
      
    #def Ok(self):
    #    global LastLieferschein
    #    self.busy(True)
    #    lf = libs.send.NeuerLieferschein()
    #    LastLieferschein = lf["identification"]
    #    libs.BlueFunc.BlueSave("LastLieferschein", LastLieferschein, "DATA/DATA")
    #    self.GetLieferschein()
    #    self.busy(False)
 
    def AddLinie(self):
        global DATA
           
        self.busy(True)

        NeueLinie = "0"
        while True:
            if not NeueLinie in DATA["linien"].split("|"):
                break
            NeueLinie = str(int(NeueLinie) + 1)

        print("Neue linie: " + str(NeueLinie))
    
        DATA["linien"] = DATA["linien"] + "|" + str(NeueLinie)
        DATA["anzahl"] = DATA["anzahl"] + "|1"
        DATA["bcode"] = DATA["bcode"] + "|"
        DATA["name"] = DATA["name"] + "|"
        DATA["preis"] = DATA["preis"] + "|0.0"

        
        while not libs.send.SetLieferschein(DATA):
            self.busy(False)

    def LinieEntfernen(self, linie):
        global DATA
        global LastLieferschein
        print("LinieEntfernen " + str(linie))

        self.busy(True)

        listdata = DATA["linien"].split("|")
        del listdata[-1]
        DATA["linien"] = "|".join(listdata)
        
        for mode in ["anzahl", "bcode", "name", "preis"]:
            listdata = DATA[mode].split("|")
            print("remove listdata:" + str(linie) + ":" + str(mode) + ":" + str(listdata))
            del listdata[linie]
            DATA[mode] = "|".join(listdata)

        while not libs.send.SetLieferschein(DATA):
            self.busy(True) 

        self.GetLieferschein()
        self.busy(False)

    def NeuerLieferschein(self):
        global DATA
        global LastLieferschein

        print("NeuerLieferschein")

        self.busy(True)

        DATA = libs.send.NeuerLieferschein()

        LastLieferschein = DATA["identification"]
        libs.BlueFunc.BlueSave("LastLieferschein", LastLieferschein, "DATA/DATA")
        self.busy(False)
 
    def GetLieferschein(self):
        global DATA
        global LastLieferschein
        print("GetLieferschein")
       
        self.busy(True)
 
        LastLieferschein = str(libs.BlueFunc.BlueLoad("LastLieferschein", "DATA/DATA"))
        print("LastLieferschein: " + str(LastLieferschein))
        if LastLieferschein == "None": self.NeuerLieferschein()

        summeTotal = 0.0
        DATA = libs.send.GetLieferschein(LastLieferschein)
        if DATA == {}:
            self.NeuerLieferschein()
        Antwort = []
        for linie in DATA["linien"].split("|"):
            linie = int(linie)
            Antwort.append({"linie":linie, "anzahl":DATA["anzahl"].split("|")[linie], "bcode":DATA["bcode"].split("|")[linie], "name":DATA["name"].split("|")[linie], "preis":DATA["preis"].split("|")[linie]})
            #try: summeTotal = summeTotal + float(DATA["anzahl"].split("|")[linie])*float(DATA["preis"].split("|")[linie])
            #except: True
        #summeTotal = float(DATA["total"])
        #DATA["total"] = summeTotal   
        summeTotal = str(DATA["total"]) + " €"
        pyotherside.send("antwortGetLieferschein", Antwort, summeTotal, DATA["fertig"])
        self.busy(False)

    def SetLieferschein(self, mode, linie, variable):
        global DATA
        global LastLieferschein
        #antwort = ""

        print("SetLieferschein linie " + str(linie))
       
        self.busy(True)
 
        if mode == "anzahl":
            listdata = DATA[mode].split("|")
            listdata[linie] = str(variable)
            DATA[mode] = "|".join(listdata)
        if mode == "bcode":
            if not str(variable) == "":
                listdata = DATA[mode].split("|")
                listdata[linie] = str(variable)
                DATA[mode] = "|".join(listdata)
                try:
                    artikel = libs.send.GetArt(str(variable))
                    
                    listdata = DATA["name"].split("|")
                    listdata[linie] = artikel["name_de"]
                    DATA["name"] = "|".join(listdata)
                    
                    listdata = DATA["preis"].split("|")
                    listdata[linie] = str(artikel["preisvk"])
                    DATA["preis"] = "|".join(listdata)
                except:
                    listdata = DATA["name"].split("|")
                    listdata[linie] = ""
                    DATA["name"] = "|".join(listdata)
                    
                    listdata = DATA["preis"].split("|")
                    listdata[linie] = ""
                    DATA["preis"] = "|".join(listdata)

        if mode == "name":
            listdata = DATA[mode].split("|")
            listdata[linie] = str(variable)
            DATA[mode] = "|".join(listdata)

        if mode == "preis":
            listdata = DATA[mode].split("|")
            listdata[linie] = str(variable).replace(",", ".")
            DATA[mode] = "|".join(listdata)

        summeTotal = 0.0
        for linie in DATA["linien"].split("|"):
            linie = int(linie)
            try: summeTotal = summeTotal + float(DATA["anzahl"].split("|")[linie])*float(DATA["preis"].split("|")[linie])
            except: True
        summeTotal = libs.RoundUp.RoundUp05(summeTotal)
        DATA["total"] = summeTotal 

        while not libs.send.SetLieferschein(DATA):
            self.busy(True)        

        self.GetLieferschein()
        self.busy(False)

    def GetIdentification(self):
        global DATA
        return DATA["identification"]

    def Fertig(self, status):
        global DATA
        print("Fertig")
        DATA["fertig"] = status
        libs.send.SetLieferschein(DATA)

    def isPhone(self):
        if os.path.exists("/home/phablet"):
            handy = True
            pyotherside.send("ifPhone", handy)
        else: handy = False
        print("isPhone: " + str(handy))
        self.busy(False)
    
        
main = Main()

