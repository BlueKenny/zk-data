#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
import os

if os.path.exists("/home/phablet"):
	DIR = "/home/phablet/.local/share/zk-data.stock/"
	from BlueFunc import *
	from debug import *
else:
	DIR = ""
	from .BlueFunc import *
	from .debug import *

BlueMkDir(DIR + "DATA")
import json

from peewee import *
local_db = SqliteDatabase("DATA/cache.db")


class Artikel(Model):# All Str are upper()
    identification = CharField(primary_key = True)
    name = CharField(null = True)
    artikel = CharField(null = True)
    artikel2 = CharField(null = True)
    artikel3 = CharField(null = True)
    artikel4 = CharField(null = True)
    barcode = IntegerField(null = True)
    lieferant = CharField(null = True)
    preisek = FloatField(null = True)
    preisvkh = FloatField(null = True)
    preisvk = FloatField(null = True)
    anzahl = FloatField(null = True)
    ort = CharField(null = True)
    lastchange = CharField(null = True)
    creation = CharField(null = True)
    minimum = FloatField(null = True)

    class Meta:
        database = local_db


local_db.connect()
try: local_db.create_tables([Artikel])
except: print("Artikel table exists")
local_db.close()

if BlueLoad("SERVERSTOCK", DIR + "DATA/DATA") == None: BlueSave("SERVERSTOCK", "127.0.0.1", DIR + "DATA/DATA")
if BlueLoad("SERVERPREISVORSCHLAG", DIR + "DATA/DATA") == None: BlueSave("SERVERPREISVORSCHLAG", "127.0.0.1", DIR + "DATA/DATA")

#SERVER_IP = ("10.0.0.1", 10000)#(BlueLoad("SERVER", "DATA/DATA"), 10000)
SERVERSTOCK_IP = (BlueLoad("SERVERSTOCK", DIR + "DATA/DATA"), 10000)
SERVERPREISVORSCHLAG_IP = (BlueLoad("SERVERPREISVORSCHLAG", DIR + "DATA/DATA"), 10001)

##############          LOCAL
def GetArtLocal(ID):# return object
    local_db.connect()
    query = Artikel.select().where(Artikel.identification == str(ID))
    if not query.exists():
        ThisArtikel = Artikel.create(name="",
                                     artikel="",
                                     artikel2="",
                                     artikel3="",
                                     artikel4="",
                                     barcode=0,
                                     lieferant="",
                                     preisek=0.0,
                                     preisvkh=0.0,
                                     preisvk=0.0,
                                     anzahl=0.0,
                                     minimum=0.0,
                                     ort="",
                                     lastchange="",
                                     creation="",
                                     identification=str(ID))
        ThisArtikel.save()
    object = Artikel.get(Artikel.identification == str(ID))
    local_db.close()
    return object

##############          STOCK

def GetArt(ID):#return object
    if True:#try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetArt"}
        ID = str(ID)
        if "P" in ID:
            sock.connect(SERVERPREISVORSCHLAG_IP)
            Dict["identification"] = str(ID[1:])
        else:
            sock.connect(SERVERSTOCK_IP)
            Dict["identification"] = str(ID)

        Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        if "P" in ID: sock.sendto(data, SERVERPREISVORSCHLAG_IP)
        else: sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        Debug("Get " + str(data))

        local_db.connect()
        query = Artikel.select().where(Artikel.identification == str(data["identification"]))
        if not query.exists():
            ThisArtikel = Artikel.create(name=data["name"],
                                         artikel=data["artikel"],
                                         artikel2=data["artikel2"],
                                         artikel3=data["artikel3"],
                                         artikel4=data["artikel4"],
                                         barcode=data["barcode"],
                                         lieferant=data["lieferant"],
                                         preisek=data["preisek"],
                                         preisvkh=data["preisvkh"],
                                         preisvk=data["preisvk"],
                                         anzahl=data["anzahl"],
                                         minimum=data["minimum"],
                                         ort=data["ort"],
                                         lastchange=data["lastchange"],
                                         creation=data["creation"],
                                         identification=data["identification"])
        else:
            ThisArtikel = Artikel(name=data["name"],
                                         artikel=data["artikel"],
                                         artikel2=data["artikel2"],
                                         artikel3=data["artikel3"],
                                         artikel4=data["artikel4"],
                                         barcode=data["barcode"],
                                         lieferant=data["lieferant"],
                                         preisek=data["preisek"],
                                         preisvkh=data["preisvkh"],
                                         preisvk=data["preisvk"],
                                         anzahl=data["anzahl"],
                                         minimum=data["minimum"],
                                         ort=data["ort"],
                                         lastchange=data["lastchange"],
                                         creation=data["creation"],
                                         identification=data["identification"])
        ThisArtikel.save()
        local_db.close()
        return ThisArtikel
    #except:
    #    return {}

def SearchArt(Dict):# Give Dict with search return Dict
    if True:#try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)

        Dict["mode"]="SearchArt"
        data = json.dumps(Dict)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        Debug("Get " + str(data))
        return data
    #except:
    #    return {}

def GetStockZahl():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERSTOCK_IP)
        data = "GetStockZahl"

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        Debug("Get " + str(data))
        sock.close()
        return json.loads(data)
    except:
        return 0

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

def SuchePreisvorschlag(suche, lieferant):#NEU
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERPREISVORSCHLAG_IP)
        Debug("Suche " + str(suche))
        Debug("Lieferant " + str(lieferant))

        data = "SuchePreisvorschlag(zKz)" + str(suche) + "(zkz)" + str(lieferant)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERPREISVORSCHLAG_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        data = data.decode()
        Dict = {}
        for each in data.split("<K>"):
            Dict[each.split("|")[0]] = str(each.split("|")[1])
        return Dict
    except:
        return {}

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

def GetArtPreisvorschlag(ID):#NEU
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVERPREISVORSCHLAG_IP)

        data = "GetArt(zKz)" + str(ID)

        Debug("Send " + str(data))
        data = data.encode()
        sock.sendto(data, SERVERPREISVORSCHLAG_IP)
        data = sock.recv(2048)
        Debug("Get " + str(data.decode()))
        sock.close()
        data = data.decode()
        Dict = {}
        for each in data.split("|"):
            Dict[each.split("&zKz&")[0]] = each.split("&zKz&")[1]

        return Dict
    except:
        return {}

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



