#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import platform
import socket
import os
from libs.barcode import *
import base64

if False:#os.path.exists("/home/phablet"):
	DIR = "/home/phablet/.local/share/zk-data.stock/"
	from .BlueFunc import *
	from .debug import *
else:
	DIR = ""
	from .BlueFunc import *
	from .debug import *

BlueMkDir(DIR + "DATA")
import json

if BlueLoad("SERVERSTOCK", DIR + "DATA/DATA") == None: BlueSave("SERVERSTOCK", "127.0.0.1", DIR + "DATA/DATA")

SERVERSTOCK_IP = (BlueLoad("SERVERSTOCK", DIR + "DATA/DATA"), 10000)
SERVERIMAGE_IP = (BlueLoad("SERVERSTOCK", DIR + "DATA/DATA"), 12345)
#####           BILDER

def SendBild(bild):
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    s.connect(SERVERIMAGE_IP)
    print("Bild ist " + str(bild))
    f = open(bild, "rb")

    s.send((host + "-" + bild).encode())
    print('Sending...')
    l = f.read(1024)
    while (l):
        print('Sending...')
        s.send(l)
        l = f.read(1024)
    f.close()
    print("Done Sending")
    s.close                     # Close the socket when done


##############          STOCK

def NeuerLieferschein():#return Dict
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"NeuerLieferschein"}
        sock.connect(SERVERSTOCK_IP)

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))

        print("NeuerLieferschein() = " + str(data))
        return data
    except:
        print("NeuerLieferschein() = ERROR")
        return {}

def GetLieferschein(ID):#return Dict
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetLieferschein"}
        ID = str(ID)
        sock.connect(SERVERSTOCK_IP)
        Dict["identification"] = ID

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))

        print("GetLieferschein(" + str(ID) + ") = " + str(data))
        return data
    except:
        print("GetLieferschein(" + str(ID) + ") = ERROR")
        return {}


def SetLieferschein(Dict):#return Bool
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        Dict["mode"] = "SetLieferschein"
        sock.connect(SERVERSTOCK_IP)

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))
        print("SetLieferschein(" + str(Dict) + ") = " + str(data))
        return data
    except:
        print("SetLieferschein(" + str(Dict) + ") = ERROR")
        return False


def GetArt(ID):#return Dict
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetArt"}
        ID = str(ID)
        sock.connect(SERVERSTOCK_IP)
        if len(ID) == 13 or len(ID) == 12:
            Dict["barcode"] = int(ID)
        else:
            Dict["identification"] = str(ID)

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))

        print("GetArt(" + str(ID) + ") = " + str(data))
        return data
    except:
        print("GetArt(" + str(ID) + ") = ERROR")
        return {}


def SetArt(Dict):#return Bool
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict["mode"] = "SetArt"
        ID = Dict["identification"]
        sock.connect(SERVERSTOCK_IP)
        Dict["identification"] = str(ID)

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))
        print("SetArt(" + str(Dict) + ") = " + str(data))
        return data
    except:
        print("SetArt(" + str(Dict) + ") = False")
        return False



def GetID():#return Dict
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetID"}
        sock.connect(SERVERSTOCK_IP)

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))

        print("GetID() = " + str(data))
        return data
    except:
        print("GetID() = ERROR")
        return {}

def AddArt(ID, Anzahl):#return Bool of sucess
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"AddArt"}
        Dict["identification"] = str(ID)
        Dict["add"] = str(Anzahl)
        sock.connect(SERVERSTOCK_IP)

        #Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))

        print("AddArt(" + str(ID) + ", " + str(Anzahl) + ") = " + str(data))
        return data
    except:
        print("AddArt(" + str(ID) + ", " + str(Anzahl) + ") = ERROR")
        return False

def SearchArt(Dict):# Give Dict with Search return List of IDs
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)

        Dict["mode"]="SearchArt"
        data = json.dumps(Dict)

        #Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))
        print("SearchArt(" + str(Dict) + ") = " + str(data))
        return data
    except:
        print("SearchArt(" + str(Dict) + ") = ERROR")
        return []

def SearchLieferschein(Dict):# Give Dict with Search return List of IDs
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)

        Dict["mode"]="SearchLieferschein"
        data = json.dumps(Dict)

        #Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        #Debug("Get " + str(data))
        print("SearchLieferschein(" + str(Dict) + ") = " + str(data))
        return data
    except:
        print("SearchLieferschein(" + str(Dict) + ") = ERROR")
        return []
