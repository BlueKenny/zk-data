#!/usr/bin/env python3

import os
import threading
import time

import pyotherside
import libs.send

from playhouse.shortcuts import model_to_dict, dict_to_model

class Main:
    def __init__(self):
        print("init")
        
    def p(self, text):
        print(text)
        
    def SearchArt(self, suche):
        if not suche == "":
            Antwort = []
            IDList = libs.send.SearchArt({"suche": suche, "lieferant": "", "ort": ""})
            for ID in IDList:
                Dict = model_to_dict(libs.send.GetArt(str(ID)))
                if "P" in Dict["identification"]:
                    Dict["farbe"] = "orange"
                else:
                    Dict["farbe"] = "blue"
                
                Antwort.append(Dict)
            pyotherside.send("antwortSearchArt", Antwort) 

main = Main()

