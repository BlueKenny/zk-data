#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send
import libs.BlueFunc

#os.system("export MIR_SOCKET=/var/run/mir_socket")

LastLieferschein = ""

class Main:    
    def __init__(self):
        global DATA
        global LastLieferschein
        print("init")
        #for user in os.listdir("/home/"):
        #    print(user)
        User = os.popen("echo $USER").readlines()[0].rstrip()
        
        if os.path.exists("/home/phablet"): Desktop = "/home/phablet/.local/share/applications"
        else: Desktop = os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip()
        
        file = Desktop + "/Kasse.desktop"
        #os.system("rm " + file)
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

        DATA = {}
        LastLieferschein = str(libs.BlueFunc.BlueLoad("LastLieferschein", "DATA/DATA"))
        print("LastLieferschein: " + str(LastLieferschein))
        if LastLieferschein == "None": self.NeuerLieferschein()
        
        self.GetLieferschein()   

    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
      
    def Ok(self):
        global LastLieferschein
        self.busy(True)
        lf = libs.send.NeuerLieferschein()
        LastLieferschein = lf["identification"]
        libs.BlueFunc.BlueSave("LastLieferschein", LastLieferschein, "DATA/DATA")
        self.GetLieferschein()
        self.busy(False)
 
    def AddLinie(self):
        global DATA
           
        self.busy(True)

        NeueLinie = "0"
        while True:
            if not NeueLinie in DATA["linien"].split("|"):
                break
            NeueLinie = str(int(NeueLinie) + 1)

        print("Neue linie: " + str(NeueLinie))
    
        DATA["linien"] = DATA["linien"] + "|" + str(NeueLinie)
        DATA["anzahl"] = DATA["anzahl"] + "|1"
        DATA["bcode"] = DATA["bcode"] + "|"
        DATA["name"] = DATA["name"] + "|"
        DATA["preis"] = DATA["preis"] + "|0.0"

        
        while not libs.send.SetLieferschein(DATA):
            self.busy(False)

    def LinieEntfernen(self, linie):
        global DATA
        global LastLieferschein
        print("LinieEntfernen " + str(linie))

        self.busy(True)

        listdata = DATA["linien"].split("|")
        del listdata[-1]
        DATA["linien"] = "|".join(listdata)
        
        for mode in ["anzahl", "bcode", "name", "preis"]:
            listdata = DATA[mode].split("|")
            print("remove listdata:" + str(linie) + ":" + str(mode) + ":" + str(listdata))
            del listdata[linie]
            DATA[mode] = "|".join(listdata)

        while not libs.send.SetLieferschein(DATA):
            self.busy(True) 

        self.GetLieferschein()
        self.busy(False)

    def NeuerLieferschein(self):
        global DATA
        global LastLieferschein

        print("NeuerLieferschein")

        self.busy(True)

        DATA = libs.send.NeuerLieferschein()

        LastLieferschein = DATA["identification"]
        libs.BlueFunc.BlueSave("LastLieferschein", LastLieferschein, "DATA/DATA")
        self.busy(False)
 
    def GetLieferschein(self):
        global DATA
        global LastLieferschein
        print("GetLieferschein")
       
        self.busy(True)
 
        DATA = libs.send.GetLieferschein(LastLieferschein)
        if DATA == {}:
            self.NeuerLieferschein()
        Antwort = []
        for linie in DATA["linien"].split("|"):
            linie = int(linie)
            #print("linie: " + str(linie))
            Antwort.append({"linie":linie, "anzahl":DATA["anzahl"].split("|")[linie], "bcode":DATA["bcode"].split("|")[linie], "name":DATA["name"].split("|")[linie], "preis":DATA["preis"].split("|")[linie]})
            #print("linie " + str(linie))        
        pyotherside.send("antwortGetLieferschein", Antwort)
        self.busy(False)

    def SetLieferschein(self, mode, linie, variable):
        global DATA
        global LastLieferschein
        #antwort = ""

        print("SetLieferschein linie " + str(linie))
       
        self.busy(True)
 
        if mode == "anzahl":
            listdata = DATA[mode].split("|")
            listdata[linie] = str(variable)
            DATA[mode] = "|".join(listdata)
        if mode == "bcode":
            if not str(variable) == "":
                listdata = DATA[mode].split("|")
                listdata[linie] = str(variable)
                DATA[mode] = "|".join(listdata)
                try:
                    artikel = libs.send.GetArt(str(variable))
                    
                    listdata = DATA["name"].split("|")
                    listdata[linie] = artikel["name_de"]
                    DATA["name"] = "|".join(listdata)
                    
                    listdata = DATA["preis"].split("|")
                    listdata[linie] = str(artikel["preisvk"])
                    DATA["preis"] = "|".join(listdata)
                except:
                    listdata = DATA["name"].split("|")
                    listdata[linie] = ""
                    DATA["name"] = "|".join(listdata)
                    
                    listdata = DATA["preis"].split("|")
                    listdata[linie] = ""
                    DATA["preis"] = "|".join(listdata)

        if mode == "name":
            listdata = DATA[mode].split("|")
            listdata[linie] = str(variable)
            DATA[mode] = "|".join(listdata)

        if mode == "preis":
            listdata = DATA[mode].split("|")
            listdata[linie] = str(variable).replace(",", ".")
            DATA[mode] = "|".join(listdata)

        while not libs.send.SetLieferschein(DATA):
            self.busy(True)        

        self.GetLieferschein()
        self.busy(False)

    def isPhone(self):
        if os.path.exists("/home/phablet"):
            handy = True
            pyotherside.send("ifPhone", handy)
        else: handy = False
        print("isPhone: " + str(handy))
        self.busy(False)
    
        
main = Main()

