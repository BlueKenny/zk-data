#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send
import libs.BlueFunc

class Main:    
    def __init__(self):
        print("init")
            
        self.busy(False)

    def LastLieferschein(self, text):
        text = text.split(", Kunde: ")[0]
        print("LastLieferschein " + str(text))
        libs.BlueFunc.BlueSave("LastLieferschein", text, "DATA/DATA")    

    def SearchKunden(self, identification, name):
        print("SearchKunden")
        if identification == "" and name == "":
            print("Keine Kunden Suche gestartet")
            listeDerElemente = []
        else:
            Dict = {}
            Dict["identification"] = str(identification)
            Dict["name"] = name
            
            listeDerElemente = libs.send.SearchKunden(Dict)

        Antwort = []    
        for item in listeDerElemente:
            DATA = libs.send.GetKunden(str(item))
            Antwort.append(DATA)
        pyotherside.send("antwortSearchKunden", Antwort)    

    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
        
main = Main()

