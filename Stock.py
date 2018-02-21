#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send

os.system("export MIR_SOCKET=/var/run/mir_socket")
# apt-get update
# apt-get install git
# qml-module-qtquick2
# qml-module-qtquick-controls
# pyotherside
#git clone https://github.com/BlueKenny/zk-data.git

class Main:    
    def __init__(self):
        print("init")
        #for user in os.listdir("/home/"):
        #    print(user)
        User = os.popen("echo $USER").readlines()[0].rstrip()
        
        if os.path.exists("/home/phablet"): Desktop = "/home/phablet/.local/share/applications/"
        else: Desktop = os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip()
        
        file = Desktop + "/Stock.desktop"
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
            
        update = os.popen("git pull").readlines()
        if not len(update) == 1:
            pyotherside.send("antwortSearchArt", {"name_de":"Bitte neustarten"}) 
        
    
    def busy(self, status):
        print("busy = " + str(status))
        status = bool(status)
        pyotherside.send("busy", status)
    def busy2(self, status):
        print("busy2 = " + str(status))
        status = bool(status)
        pyotherside.send("busy2", status)
        
    def GetArt(self, ID):
        print("antwortGetArt")
        self.busy2(True)
        Dict = libs.send.GetArt(str(ID))
        del Dict["identification"]
        Antwort = []
        for text, var in Dict.items():
            Antwort.append({"name": str(text) + ": " + str(var)})
        pyotherside.send("antwortGetArt", Antwort)
        self.busy2(False)
        
    
    def SearchArt(self, suche):
        self.busy(True)
        if not suche == "":
            Antwort = []
            IDList = libs.send.SearchArt({"suche": suche, "ort": "", "lieferant": ""})
            for ID in IDList:
                Dict = libs.send.GetArt(str(ID))
                Antwort.append(Dict)
            pyotherside.send("antwortSearchArt", Antwort) 
        self.busy(False)

    def isPhone(self):
        if os.path.exists("/home/phablet"): handy = True
        else: handy = True
        print("isPhone: " + str(handy))
        pyotherside.send("ifPhone", handy)
        self.busy(False)
    
    def isPhone2(self):
        if os.path.exists("/home/phablet"): handy = True
        else: handy = True
        print("isPhone2: " + str(handy))
        pyotherside.send("ifPhone2", handy)
        self.busy2(False)
        
main = Main()

