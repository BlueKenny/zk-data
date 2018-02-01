#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
import os
from BlueFunc import *
from debug import *

if os.path.exists("/home/phablet"):
	DIR = "/home/phablet/.local/share/zk-data.stock/"
else: DIR = ""

BlueMkDir(DIR + "DATA")

if BlueLoad("SERVERSTOCK", DIR + "DATA/DATA") == None: BlueSave("SERVERSTOCK", "127.0.0.1", DIR + "DATA/DATA")
if BlueLoad("SERVERPREISVORSCHLAG", DIR + "DATA/DATA") == None: BlueSave("SERVERPREISVORSCHLAG", "127.0.0.1", DIR + "DATA/DATA")

#SERVER_IP = ("10.0.0.1", 10000)#(BlueLoad("SERVER", "DATA/DATA"), 10000)
SERVERSTOCK_IP = (BlueLoad("SERVERSTOCK", DIR + "DATA/DATA"), 10000)
SERVERPREISVORSCHLAG_IP = (BlueLoad("SERVERPREISVORSCHLAG", DIR + "DATA/DATA"), 10001)

##############          STOCK
def GetStockZahl():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)
        data = "GetStockZahl"

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        return int(data.decode())
    except:
        return 0

def SendeSucheStock(suche, ort, lieferant):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)
        Debug("Suche " + str(suche))
        Debug("Ort " + str(ort))
        Debug("Lieferant " + str(lieferant))

        data = "SearchStock(zKz)" + str(suche) + "(zkz)" + str(ort) + "(zkz)" + str(lieferant)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        return data.decode()
    except:
        return "0<K>"


def StockGetArtInfo(Vars, IDToChange):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)

        data = "GetArtInfo(zKz)" + str(IDToChange)
        for Var in Vars:
            data = data + "(zkz)" + str(Var)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        return data.decode()
    except:
        SendThis = str(IDToChange)
        for each in Vars:
            SendThis = SendThis + " | "
        return SendThis

def StockSetArtInfo(IDToChange, VarName, Var):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVERSTOCK_IP)
    data = "StockSetArtInfo(zKz)" + str(IDToChange) + "(zkz)" + str(VarName) + "(zkz)" + str(Var)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVERSTOCK_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def StockGetBewegung(ID):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVERSTOCK_IP)
    data = "StockGetBewegung(zKz)" + str(ID)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVERSTOCK_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def StockSetBCode():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVERSTOCK_IP)
    data = "StockSetBCode(zKz)"

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVERSTOCK_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def SendeChangeAnzahl(bcode, anzahl):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVERSTOCK_IP)
    Debug("Bcode " + str(bcode))
    Debug("Anzahl " + str(anzahl))

    data = "ChangeStock(zKz)" + str(bcode) + "(zkz)" + str(anzahl)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVERSTOCK_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

##############          PREISVORSCHLAG
def GetStockPreisvorschlagAnzahl():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERPREISVORSCHLAG_IP)
        data = "GetStockZahl"

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERPREISVORSCHLAG_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        return int(data.decode())
    except:
        return 0

def SendeSuchePreisvorschlag(suche, lieferant):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERPREISVORSCHLAG_IP)
        Debug("Suche " + str(suche))
        Debug("Lieferant " + str(lieferant))

        data = "SearchStock(zKz)" + str(suche) + "(zkz)" + str(lieferant)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERPREISVORSCHLAG_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        return data.decode()
    except:
        return "0<K>"

def PreisvorschlagGetArtInfo(Vars, IDToChange):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERPREISVORSCHLAG_IP)

        IDToChange = IDToChange.replace("P", "")
        data = "GetArtInfo(zKz)" + str(IDToChange)
        for Var in Vars:
            data = data + "(zkz)" + str(Var)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERPREISVORSCHLAG_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        return data.decode()
    except:
        SendThis = IDToChange
        for each in Vars: SendThis = IDToChange + " | "
        return SendThis





#SERVER_IP_LIST=BlueLoad("SERVER", "DATA/DATA").split("|")

#SERVER_IP = (0, 10000)
#while SERVER_IP == (0, 10000):
#	for IPX in SERVER_IP_LIST:
#		try:
#			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#			sock.connect((IPX, 10000))
#			SERVER_IP = (IPX, 10000)
#			print("Verbindung mit : " + str(IPX))
#			break
#		except Exception as e:
#			print("Keine verbindung : " + str(IPX))
#		finally:
#			sock.close()

#### OLD    OLD             OLD

def SendeSaveArbeiterLinie(Arbeiter, Linie, Text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "SaveArbeiterLinie(zKz)" + str(Arbeiter) + "(zkz)" + str(Linie) + "(zkz)" + str(Text)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def SendeGetArbeiterLinie(Arbeiter, Linie):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "GetArbeiterLinie(zKz)" + str(Arbeiter) + "(zkz)" + str(Linie)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def GetListeDerArbeiter():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "ListeDerArbeiter"

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def NeueKundenID():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "NeueKundenID"

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def KundeGetInfo(Var, IDToChange):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "KundeGetInfo(zKz)" + str(IDToChange) + str(Var)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def KundeSetInfo(IDToChange, VarName, Var):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "KundeSetInfo(zKz)" + str(IDToChange) + "(zkz)" + str(VarName) + "(zkz)" + str(Var)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def GetKundenZahl():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    data = "GetKundenZahl"

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()

def SendeSucheKunde(suche, tel, ort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_IP)
    Debug("Suche " + str(suche))
    Debug("Tel " + str(tel))
    Debug("Ort " + str(ort))

    data = "SearchKunde(zKz)" + str(suche) + "(zkz)" + str(tel) + "(zkz)" + str(ort)

    Debug("Send " + str(data))
    data = data.encode()
    sock.sendto(data, SERVER_IP)
    data = sock.recv(2048)
    Debug("Get " + str(data.decode()))
    sock.close()
    return data.decode()



