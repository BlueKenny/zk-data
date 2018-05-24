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
        self.busy(False)
        self.checkStats(1)
        
    def checkStats(self, Monat):
        print("checkStats(" + str(Monat) + ")") 

        Liste = []
        for x in range(1,32):
            if x < 10: x = "0" + str(x)
            Monat = str(Monat).split(".")[0]
            if len(Monat) < 2: Monat = "0" + Monat
            TagFloat = float(libs.send.GetGewinn("2018-" + Monat + "-" + str(x)))
            Liste.append(TagFloat)
        pyotherside.send("antwortStats", Liste)
    
    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
        
main = Main()

