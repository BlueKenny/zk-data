#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send

os.system("export MIR_SOCKET=/var/run/mir_socket")

DATA = {}
#DATA["datum"] = "0"
#DATA["linien"] = []
#DATA["anzahl"] = []
#DATA["bcode"] = []
#DATA["name"] = []
#DATA["preis"] = []
# str = "/".join(liste1)

class Main:    
    def __init__(self):
        global DATA
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


        #if DATA["linien"] == []:
        #    self.AddLinie()
        self.GetLieferschein()   

    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
    def busy2(self, status):
        status = bool(status)
        print("busy2 = " + str(status))
        pyotherside.send("busy2", status)
       
    def AddLinie(self):
        global DATA
           
        self.busy2(True)

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
            self.busy2(False)
 
    def GetLieferschein(self):
        global DATA
        print("GetLieferschein")
       
        self.busy2(True)
 
        DATA = libs.send.GetLieferschein("1")

        Antwort = []
        for linie in DATA["linien"].split("|"):
            linie = int(linie)
            print("linie: " + str(linie))
            Antwort.append({"linie":linie, "anzahl":DATA["anzahl"].split("|")[linie], "bcode":DATA["bcode"].split("|")[linie], "name":DATA["name"].split("|")[linie], "preis":DATA["preis"].split("|")[linie]})
            print("linie " + str(linie))        
        pyotherside.send("antwortGetLieferschein", Antwort)
        self.busy2(False)

    def SetLieferschein(self, mode, linie, variable):
        global DATA
        #antwort = ""

        print("SetLieferschein linie " + str(linie))
       
        self.busy2(True)
 
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
            #try:
            #    float(listdata[linie])
            #    farbe = "green"
            #except:            
            #    farbe = "red"

        while not libs.send.SetLieferschein(DATA):
            self.busy2(True)        

        self.GetLieferschein()
        self.busy2(False)

        return "red"
            
    
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

