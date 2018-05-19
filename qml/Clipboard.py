#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True
import libs.send
import libs.BlueFunc

try: import pyperclip
except:
    print("Start pyperclip installation")
    os.system("pip3 install --user pyperclip")
    import pyperclip
#pyperclip.paste()
#pyperclip.copy(text)


class Main:    
    def __init__(self):
        self.busy(False)
        self.oldclipboard = ""
        
    def checkClipboard(self):
        print("checkClipboard") 
        newclipboard = pyperclip.paste()
        if not self.oldclipboard == newclipboard:
            print(newclipboard)
            Liste = []
            ArtList = libs.send.SearchArt({"suche": str(newclipboard)})
            print("ArtList: " + str(ArtList))
            for eachID in ArtList:
                ThisArtikel = libs.send.GetArt(eachID)
                if not "P" in ThisArtikel["identification"]:
                    Liste.append(ThisArtikel)
                
            pyotherside.send("antwortClipboard", Liste)
            print(Liste)
            self.oldclipboard = newclipboard
    
    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
        
main = Main()

