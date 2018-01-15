#!/usr/bin/env python3
import sys
import socket
#from libs.BlueFunc import *
#from libs.debug import *

def PrintBarcode(IP, ID, Barcode, Name, Price):
	TCP_IP = "192.168.188.67"
	TCP_PORT = 9100

	ID = str(ID)
	Barcode = str(Barcode)
	Name = str(Name)
	Price = str(Price) + " Euro"

	BarcodePos = "^FO140,5^BY2"
	BarcodeType = "^BEI,30,N,N"
	BarcodeString = "^FD" + Barcode + "^FS"
	Barcode = BarcodePos + BarcodeType + BarcodeString

	IDPos = "^FO120,30^BY3"
	IDText = "^AOB^FD" + ID + "^FS"
	ID = IDPos + IDText

	MaxStringLen = 32
	if len(Name) < MaxStringLen:
		NamePos = "^FO150,80^BY1"
		NameText = "^AON^FD" + Name + "^FS"
		Name = NamePos + NameText
	else:
		Name1 = Name[0:MaxStringLen]
		Name2 = Name[MaxStringLen:len(Name)]
		NamePos1 = "^FO150,80^BY1"
		NameText1 = "^AON^FD" + Name1 + "^FS"
		NamePos2 = "^FO150,110^BY1"
		NameText2 = "^AON^FD" + Name2 + "^FS"
		Name = NamePos1 + NameText1 + NamePos2 + NameText2
	

	PricePos = "^FO160,40^BY1"
	PriceText = "^AON^FD" + Price + "^FS"
	Price = PricePos + PriceText

	zpl="^XA" + Barcode + ID + Name + Price + "^XZ"
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(bytes(zpl, "utf-8"))
	s.close()


def PrintLocation(Location):
	TCP_IP = "192.168.188.67"
	TCP_PORT = 9100

	Location = str(Location)

	BarcodePos = "^FO150,10^BY1"
	BarcodeType = "^B3,Y,40,N,N"
	BarcodeString = "^FD" + Location + "^FS"
	Barcode = BarcodePos + BarcodeType + BarcodeString

	StringPos = "^FO150,70^BY3"
	StringText = "^AFD^FD" + Location + "^FS"
	String = StringPos + StringText

	zpl="^XA" + Barcode + String + "^XZ"
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(bytes(zpl, "utf-8"))
	s.close()
