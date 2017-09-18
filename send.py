#!/usr/bin/env python
import sys
import socket
from appJar import gui
from debug import * 

SERVER_IP_LIST=["raspberrypi", "localhost", "127.0.0.1"]

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


def GetMachine(index):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	data = "GetMachine(zKz)" + str(index)

	Debug("Send " + str(data))
	data = data.encode()
	sock.sendto(data, SERVER_IP)
	data = sock.recv(2048)
	Debug("Get " + str(data.decode()))
	sock.close()
	return data.decode()

def GetMachinenAnzahl():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	data = "GetMachinenAnzahl"

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
	

def SendeSucheStock(bcode, barcode, artikel, ort, machine):
	#bcode = int(bcode); barcode = str(barcode); artikel = str(artikel);
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_IP)
	Debug("Bcode " + str(bcode))
	Debug("Barcode " + str(barcode))
	Debug("Artikel " + str(artikel))
	Debug("Ort " + str(ort))
	Debug("Machine " + str(machine))
	
	data = "SearchStock(zKz)" + str(bcode) + "(zkz)" + str(barcode) + "(zkz)" + str(artikel) + "(zkz)" + str(ort) + "(zkz)" + str(machine)

	Debug("Send " + str(data))
	data = data.encode()
	sock.sendto(data, SERVER_IP)
	data = sock.recv(2048)
	Debug("Get " + str(data.decode()))
	sock.close()
	return data.decode()
	


