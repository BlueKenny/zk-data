#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send
import random

os.system("export MIR_SOCKET=/var/run/mir_socket")

class Main:    
    def __init__(self):
        print("init")
        #for user in os.listdir("/home/"):
        #    print(user)
        User = os.popen("echo $USER").readlines()[0].rstrip()
        
        if os.path.exists("/home/phablet"): Desktop = "/home/phablet/.local/share/applications"
        else: Desktop = os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip()
        
        file = Desktop + "/Kasse.desktop"
        os.system("rm " + file)
        if not os.path.exists(file):
            print("Write Desktop Entry")
            print("User: " + str(User))
            print("Desktop: " + str(Desktop))
            print("file: " + str(file))
            DesktopEntry = open(file, "a")
            DesktopEntry.write("[Desktop Entry]\n")
            DesktopEntry.write("Name=Kasse\n")
            DesktopEntry.write("Path=/home/" + User + "/zk-data/\n")
            DesktopEntry.write("Exec=qmlscene /home/" + User + "/zk-data/Kasse.qml\n")
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

        try:
            libs.send.GetBarcode("/home/phablet/Pictures/scan.jpg")
            #barcode = os.popen("zbarimg /home/phablet/Pictures/scan.jpg -q").readlines()[0]#.split(":")[1]
            print("barcode: " + str(barcode))
        except:
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
        
    def GetLieferschein(self, ID):
        print("antwortGetArt")
        DATA = {}
        DATA["datum"] = "0"
        DATA["linien"] = []
        DATA["anzahl"] = {}
        DATA["bcode"] = {}
        DATA["name"] = {}

        for x in range(1, 11):
            x = str(x)
            DATA["linien"].append(x)
            DATA["anzahl"][x] = random.randint(0, 10)
            DATA["bcode"][x] = str(random.randint(100000, 999999))
            DATA["name"][x] = "t" + str(random.randint(0, 100))
        self.busy2(True)

        Antwort = []
        for linie in DATA["linien"]:
            Antwort.append({"linie":linie, "anzahl":DATA["anzahl"][linie], "bcode":DATA["bcode"][linie], "name":DATA["name"][linie]})
        pyotherside.send("antwortGetLieferschein", Antwort)
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

