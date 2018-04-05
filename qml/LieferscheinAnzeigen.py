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
 
    #def AddLinie(self):
    #    global DATA
           
    #    self.busy(True)
        
    #    while not libs.send.SetLieferschein(DATA):
    #        self.busy(False)

    #    self.GetLieferschein()

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
        pyotherside.send("antwortGetLieferschein", Antwort, summeTotal, DATA["fertig"], DATA["kunde_id"], DATA["kunde_name"])
        self.busy(False)

    def SetLieferschein(self, linie, anzahl, bcode, name, preis):
        global DATA
        global LastLieferschein
        #antwort = ""

        print("SetLieferschein linie " + str(linie))
       
        self.busy(True)
 
        mode = "anzahl"
        variable = str(anzahl)
         
        listdata = DATA[mode].split("|")
        listdata[linie] = str(variable)
        print("Setze " + mode + " auf " + str(variable))
        DATA[mode] = "|".join(listdata)     
        
        mode = "bcode"
        variable = str(bcode)
        
        if mode == "bcode":
            if not str(variable) == "":
                listdata = DATA[mode].split("|")
                listdata[linie] = str(variable)
                DATA[mode] = "|".join(listdata)
                try:
                    artikel = libs.send.GetArt(str(variable))

                    listdata = DATA["bcode"].split("|")
                    listdata[linie] = artikel["identification"]
                    print("Setze " + mode + " auf " + str(variable))
                    DATA["bcode"] = "|".join(listdata)
                    
                    if name.rstrip() == "": name = artikel["name_de"]
                    
                    if preis == "0.0" or preis.rstrip() == "": preis = str(artikel["preisvk"])
                    
                    os.system("aplay DATA/scan-yes.wav &")
                    
                except:
                    print("Error")
                    os.system("aplay DATA/scan-no.wav &")

                    listdata = DATA[mode].split("|")
                    listdata[linie] = ""
                    print("Setze " + mode + " auf " + str(variable))
                    DATA[mode] = "|".join(listdata)

                    #listdata = DATA["name"].split("|")
                    #listdata[linie] = ""
                    #DATA["name"] = "|".join(listdata)
                    
                    #listdata = DATA["preis"].split("|")
                    #listdata[linie] = ""
                    #DATA["preis"] = "|".join(listdata)

        mode = "name"
        variable = str(name)
        
        if mode == "name":
            listdata = DATA[mode].split("|")
            print(mode + " ist " + listdata[linie])
            listdata[linie] = str(variable)
            print("Setze " + mode + " auf " + str(variable))
            DATA[mode] = "|".join(listdata)

        mode = "preis"
        variable = str(preis)
        
        if mode == "preis":
            listdata = DATA[mode].split("|")
            print(mode + " ist " + listdata[linie])
            listdata[linie] = str(variable)
            listdata[linie] = str(variable).replace(",", ".")
            print("Setze " + mode + " auf " + str(variable))
            DATA[mode] = "|".join(listdata)

        summeTotal = 0.0
        for linie in DATA["linien"].split("|"):
            linie = int(linie)
            try: summeTotal = summeTotal + float(DATA["anzahl"].split("|")[linie])*float(DATA["preis"].split("|")[linie])
            except: True
        summeTotal = libs.RoundUp.RoundUp05(summeTotal)
        DATA["total"] = summeTotal 

        #while not
        libs.send.SetLieferschein(DATA)
        #    self.busy(True)        

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

    def SetKunde(self, kunde_id):
        print("SetKunde")
        global DATA        
        global LastLieferschein
        DATA["kunde_id"] = kunde_id       
        libs.send.SetLieferschein(DATA)
        DATA = libs.send.GetLieferschein(LastLieferschein)
        return DATA["kunde_name"]
    
    def Drucken(self):
        global DATA
        from pyexcel_ods import get_data
        data = get_data("DATA/lieferschein.ods")
        import json
        dateiZumDrucken = json.dumps(data)
        print(dateiZumDrucken)

        #dateiZumDrucken = open("DATA/lieferschein", "r").read()

        #dateiZumDrucken = dateiZumDrucken.replace("datum", DATA["datum"])
        #dateiZumDrucken = dateiZumDrucken.replace("kunde_tel1", "tel1")
        #dateiZumDrucken = dateiZumDrucken.replace("kunde_name", "name")
        #dateiZumDrucken = dateiZumDrucken.replace("kunde_adresse", "adresse")
        #dateiZumDrucken = dateiZumDrucken.replace("lieferschein_nummer", DATA["identification"])

        for x in range(0, 30):
            try:
                if str(DATA["bcode"].split("|")[x]) == "": # Fehler
                    int("a")

                #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_name", DATA["name"].split("|")[x])
                #if str(DATA["bcode"].split("|")[x]) == "0" or str(DATA["bcode"].split("|")[x]) == "1":
                    #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_preis", "-")
                    #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_anzahl", "-")
                #else:
                    #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_preis", DATA["preis"].split("|")[x] + "€")
                    #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_anzahl", DATA["anzahl"].split("|")[x] + "x")
                #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_total", str(float(DATA["anzahl"].split("|")[x]) * float(DATA["preis"].split("|")[x])) + "€")
            except:
                #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_anzahl", "")
                #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_name", "")
                #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_preis", "")
                #dateiZumDrucken = dateiZumDrucken.replace(" " + str(x) + "_total", "")
                True

        #dateiZumDrucken = dateiZumDrucken.replace("end_total", str(DATA["total"]))

        from pyexcel_ods import save_data
        save_data("DATA/lieferscheinTMP.ods", dateiZumDrucken)
        #open("DATA/lieferscheinTMP", "w").write(dateiZumDrucken)
        os.system("lpr -P drucker DATA/lieferscheinTMP")
        #print(dateiZumDrucken)

    def isPhone(self):
        if os.path.exists("/home/phablet"):
            handy = True
            pyotherside.send("ifPhone", handy)
        else: handy = False
        print("isPhone: " + str(handy))
        self.busy(False)
    
        
main = Main()

