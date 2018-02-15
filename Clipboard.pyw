#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import os

try: import pyperclip
except:
    if platform.system() == "Linux":
        os.system("pip3 install --user pyperclip")

try: import notify2
except:
    if platform.system() == "Linux":
        os.system("pip3 install --user notify2")

import libs.send
import subprocess

# for autostart on windows
# copy a link in
# C:\users\<your username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

OldData = ""

print("os: " + str(platform.system()))

while True:  # def Check(): # import
    NewData = pyperclip.paste()
    NewData = NewData.upper()

    if not OldData == NewData and not NewData == "":
        print("NewData:" + str(NewData))
        OldData = NewData

        IDsAndTime = libs.send.SearchArt({"suche": NewData, "lieferant": "", "ort": ""})
        print("IDsAndTime " + str(IDsAndTime))

        for ID, Time in IDsAndTime.items():
            object = {}#libs.send.GetArt(ID)
            if object == {}:
                object = libs.send.GetArtLocal(ID)

            if not object == {}:

                Text = object.name_de + "\n"
                notify2.init("ZK-DATA")
                n = notify2.Notification("Stock", Text)
                n.show()


