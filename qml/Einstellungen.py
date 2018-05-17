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
        
    def SetDrucker(self, IP):
        IP = str(IP)
        libs.BlueFunc.BlueSave("PrinterIP", IP, "DATA/DATA")
        print("SetDrucker(" + IP + ")")
        
    def SetServer(self, IP):
        IP = str(IP)
        libs.BlueFunc.BlueSave("SERVERSTOCK", IP, "DATA/DATA")
        print("SetServer(" + IP + ")")
        
    def GetDrucker(self):
        IP = str(libs.BlueFunc.BlueLoad("PrinterIP", "DATA/DATA"))
        print("GetDrucker() = " + IP)
        return IP
        
    def GetServer(self):
        IP = str(libs.BlueFunc.BlueLoad("SERVERSTOCK", "DATA/DATA"))
        print("GetServer() = " + IP)
        return IP
        
main = Main()

