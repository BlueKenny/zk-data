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

    def GetLieferscheine(self, identification, kunde, fertige, eigene):
        print("Lieferscheine")
        Dict = {}
        Dict["identification"] = str(identification)
        Dict["kunde_id"] = str(kunde)
        Dict["fertig"] = bool(fertige)
        #Dict["user"] = str(identification)
        
        listeDerElemente = libs.send.SearchLieferschein(Dict)

        Antwort = []    
        for item in listeDerElemente:
            DATA = libs.send.GetLieferschein(str(item))
            Antwort.append(DATA)
        pyotherside.send("antwortSearchLieferscheine", Antwort)
    
    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
        
main = Main()

