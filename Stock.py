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
            
        self.busy(False)
        
    
    def busy(self, status):
        status = bool(status)
        pyotherside.send("busy", status)
        
    def SearchArt(self, suche):
        self.busy(True)
        if not suche == "":
            Antwort = []
            IDList = libs.send.SearchArt({"suche": suche, "lieferant": "", "ort": ""})
            for ID in IDList:
                Dict = libs.send.GetArt(str(ID))
                Antwort.append(Dict)
            pyotherside.send("antwortSearchArt", Antwort) 
        self.busy(False)

    def isPhone(self):
        if os.path.exists("/home/phablet"):
            print("isPhone: True")
            pyotherside.send("ifPhone", True) 
        else:
            print("isPhone: False")
            pyotherside.send("ifPhone", True) 
        
main = Main()

