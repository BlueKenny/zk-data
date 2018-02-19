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
        #for user in os.listdir("/home/"):
        #    print(user)
        User = os.popen("echo $USER").readlines()[0].rstrip()
        Desktop = os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip()
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

