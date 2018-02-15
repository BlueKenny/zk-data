#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import platform
import socket
import os
from libs.barcode import *

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

try: from peewee import *
except:
    if platform.system() == "Linux": os.system("pip3 install --user peewee")

from playhouse.shortcuts import model_to_dict, dict_to_model
local_db = SqliteDatabase("DATA/cache.db")

class Bewegung(Model):
    identification = CharField(primary_key = True)
    bcode = CharField(null = True)
    datum = CharField(null = False, default=str(Date()))
    start = FloatField(null = False, default=0)
    end = FloatField(null = False, default=0)
    preisek = FloatField(null = False, default = 0.0)
    preisvkh = FloatField(null = False, default = 0.0)
    preisvk = FloatField(null = False, default = 0.0)
    mode = CharField(null = False)
    user = CharField(null = False)

    class Meta:
        database = local_db

class Artikel(Model):# All Str are upper()
    identification = CharField(primary_key = True)
    name_de = CharField(default = "")
    name_fr = CharField(default = "")
    artikel = CharField(default = "")
    artikel2 = CharField(default = "")
    artikel3 = CharField(default = "")
    artikel4 = CharField(default = "")
    barcode = IntegerField(default=0)
    lieferant = CharField(default="")
    preisek = FloatField(default = 0.0)
    preisvkh = FloatField(default = 0.0)
    preisvk = FloatField(default = 0.0)
    anzahl = FloatField(default = 0.0)
    ort = CharField(default = "")
    lastchange = CharField(default=str(Timestamp()))
    creation = CharField(default=str(Date()))
    minimum = FloatField(default = 0.0)
    categorie = CharField(default = "")
    bild = CharField(default = "")
    beschreibung_de = TextField(default = "")
    beschreibung_fr = TextField(default = "")
    baujahr = IntegerField(default = 0)
    web = BooleanField(default = False)
    farbe = CharField(default = "")

    class Meta:
        database = local_db


local_db.connect()
try: local_db.create_tables([Artikel])
except: print("Artikel table exists")
local_db.close()

local_db.connect()
try: local_db.create_tables([Bewegung])
except: print("Bewegung table exists in local_db")
local_db.close()

if BlueLoad("SERVERSTOCK", DIR + "DATA/DATA") == None: BlueSave("SERVERSTOCK", "127.0.0.1", DIR + "DATA/DATA")
if BlueLoad("SERVERPREISVORSCHLAG", DIR + "DATA/DATA") == None: BlueSave("SERVERPREISVORSCHLAG", "127.0.0.1", DIR + "DATA/DATA")

SERVERSTOCK_IP = (BlueLoad("SERVERSTOCK", DIR + "DATA/DATA"), 10000)
SERVERPREISVORSCHLAG_IP = (BlueLoad("SERVERPREISVORSCHLAG", DIR + "DATA/DATA"), 10001)

##############          LOCAL
def GetArtLocal(ID):# return object
    local_db.connect()
    query = Artikel.select().where(Artikel.identification == str(str(ID)))
    if not query.exists():
        Artikel.create(identification=str(ID))
    object = Artikel.get(Artikel.identification == str(ID))
    local_db.close()
    return object

def GetBewegungTagLocal():# return Dict of object
    Tag = str(Date())
    local_db.connect()
    query = Bewegung.select().where(Bewegung.datum == str(Tag))
    Dict = {}
    for ID in query:
        Dict[ID.identification] = ID
    return Dict

def GetBewegungLocal(ID):# return object
    local_db.connect()
    query = Bewegung.select().where(Bewegung.identification == str(ID))
    if not query.exists():
        Bewegung.create(identification=str(ID))
    object = Bewegung.get(Bewegung.identification == str(ID))
    local_db.close()
    return object

##############          STOCK
def GetBewegung(ID): # return object
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetBewegung"}
        sock.connect(SERVERSTOCK_IP)
        Dict["identification"] = str(ID)

        Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        Debug("Get " + str(data))

        local_db.connect()
        query = Bewegung.select().where(Bewegung.identification == str(data["identification"]))
        if not query.exists():
            ThisArtikel = Bewegung.create(**data)
        else:
            ThisArtikel = dict_to_model(Bewegung, data)
        ThisArtikel.save()
        local_db.close()
        return ThisArtikel
    except:
        return {}


def GetBewegungIndex(): #return Int
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Dict = {"mode": "GetBewegungIndex"}
    sock.connect(SERVERSTOCK_IP)

    Debug("Send " + str(Dict))
    data = json.dumps(Dict)  # data serialized
    data = data.encode()
    sock.sendto(data, SERVERSTOCK_IP)
    data = sock.recv(2048)
    data = data.decode()
    data = json.loads(data)
    sock.close()
    Debug("Get " + str(data))
    return int(data)

def GetArt(ID):#return object
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetArt"}
        ID = str(ID)
        sock.connect(SERVERSTOCK_IP)
        Dict["identification"] = str(ID)

        Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        Debug("Get " + str(data))

        local_db.connect()
        query = Artikel.select().where(Artikel.identification == str(data["identification"]))
        if not query.exists():
            ThisArtikel = Artikel.create(**data)
        else:
            ThisArtikel = dict_to_model(Artikel, data)
        ThisArtikel.save()
        local_db.close()
        return ThisArtikel
    except:
        return {}


def SetArt(Dict):#return string
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict["mode"] = "SetArt"
        ID = Dict["identification"]
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
        return data
    except:
        return False



def GetID():#return object
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"GetID"}
        sock.connect(SERVERSTOCK_IP)

        Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        Debug("Get " + str(data))

        local_db.connect()
        query = Artikel.select().where(Artikel.identification == str(data["identification"]))
        if not query.exists():
            ThisArtikel = Artikel.create(**data)
        else:
            ThisArtikel = dict_to_model(Artikel, data)
        ThisArtikel.save()
        local_db.close()
        return ThisArtikel
    except:
        return {}

def AddArt(ID, Anzahl):#return object
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dict = {"mode":"AddArt"}
        Dict["identification"] = str(ID)
        Dict["add"] = str(Anzahl)
        sock.connect(SERVERSTOCK_IP)

        Debug("Send " + str(Dict))
        data = json.dumps(Dict)  # data serialized
        data = data.encode()
        sock.sendto(data, SERVERSTOCK_IP)
        data = sock.recv(2048)
        data = data.decode()
        data = json.loads(data)
        sock.close()
        Debug("Get " + str(data))

        local_db.connect()
        query = Artikel.select().where(Artikel.identification == str(data["identification"]))
        if not query.exists():
            ThisArtikel = Artikel.create(**data)
        else:
            ThisArtikel = dict_to_model(Artikel, data)
        ThisArtikel.save()
        local_db.close()
        return ThisArtikel
    except:
        return {}

def SearchArt(Dict):# Give Dict with search return Dict
    try:
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
    except:
        return {}
