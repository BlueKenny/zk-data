#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send

os.system("export MIR_SOCKET=/var/run/mir_socket")

class Main:    
    def __init__(self):
        print("init")
        #for user in os.listdir("/home/"):
        #    print(user)
        User = os.popen("echo $USER").readlines()[0].rstrip()
        
        if os.path.exists("/home/phablet"): Desktop = "/home/phablet/.local/share/applications"
        else: Desktop = os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip()
        
        file = Desktop + "/Stock.desktop"
        #os.system("rm " + file)
        if not os.path.exists(file):
            print("Write Desktop Entry")
            print("User: " + str(User))
            print("Desktop: " + str(Desktop))
            print("file: " + str(file))
            DesktopEntry = open(file, "a")
            DesktopEntry.write("[Desktop Entry]\n")
            DesktopEntry.write("Name=Stock\n")
            DesktopEntry.write("Path=/home/" + User + "/zk-data/\n")
            DesktopEntry.write("Exec=qmlscene /home/" + User + "/zk-data/Stock.qml\n")
            DesktopEntry.write("Terminal=false\n")
            DesktopEntry.write("X-Ubuntu-Touch=true\n")
            DesktopEntry.write("Type=Application\n")
            DesktopEntry.write("StartupNotify=true\n")
            DesktopEntry.write("Icon=None\n")
             
            os.system("chmod +x " + file)
            
        os.system("git pull")
        self.busy(False)
    
    def ScanForSearch(self):
        self.busy(True)

        if True:
            libs.send.SendBild("/home/phablet/Pictures/scan.jpg")
            #libs.send.GetBarcode("/home/phablet/Pictures/scan.jpg")
            barcode = "ok"
            print("barcode: " + str(barcode))
        if False:
            barcode = "nichts"
            os.system("test_vibrator")

        os.system("test_vibrator")
        pyotherside.send("antwortScanForSearch", barcode)

        self.busy(False)
    
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

