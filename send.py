#!/usr/bin/env python3
import sys
import socket
from BlueFunc import *
from debug import *


SERVER_IP_LIST=BlueLoad("SERVER", "DATA").split("|")#["warenannahmepc1", "127.0.0.1"]

SERVER_IP = (0, 10000)
while SERVER_IP == (0, 10000):
	for IPX in SERVER_IP_LIST:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((IPX, 10000)) 
			SERVER_IP = (IPX, 10000)
			print("Verbindung mit : " + str(IPX))
			break
		except Exception as e: 
			print("Keine verbindung : " + str(IPX))
		finally:
			sock.close()
	
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

def StockGetArtInfo(Var, IDToChange):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	data = "StockGetArtInfo(zKz)" + str(IDToChange) + str(Var)

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

def StockSetArtInfo(IDToChange, VarName, Var):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	data = "StockSetArtInfo(zKz)" + str(IDToChange) + "(zkz)" + str(VarName) + "(zkz)" + str(Var)

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

def GetStockZahl():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	data = "GetStockZahl"

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

	

def SendeChangeAnzahl(bcode, anzahl):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	Debug("Bcode " + str(bcode))
	Debug("Anzahl " + str(anzahl))
	
	data = "ChangeStock(zKz)" + str(bcode) + "(zkz)" + str(anzahl)

	Debug("Send " + str(data))
	data = data.encode()
	sock.sendto(data, SERVER_IP)
	data = sock.recv(2048)
	Debug("Get " + str(data.decode()))
	sock.close()
	return data.decode()
	

def SendeSucheStock(suche, ort, lieferant):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	Debug("Suche " + str(suche))
	Debug("Ort " + str(ort))
	Debug("Lieferant " + str(lieferant))

	data = "SearchStock(zKz)" + str(suche) + "(zkz)" + str(ort) + "(zkz)" + str(lieferant)

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
	


