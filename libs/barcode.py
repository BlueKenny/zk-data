#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import socket
from .BlueFunc import *

# from libs.debug import *

TCP_IP = BlueLoad("PrinterIP", "DATA/DATA")  # ZBR5581684 ##### ZBR7681522
TCP_PORT = 9100
if TCP_IP == None or TCP_IP == "None":
    TCP_IP = "ZBR7681522"
    BlueSave("PrinterIP", TCP_IP, "DATA/DATA")


def CheckBarcode(Barcode):
    print("Check Barcode")
    print("Barcode " + str(Barcode))

    if Barcode[-13] + Barcode[-12] + Barcode[-11] + Barcode[-10] == "0000":
        print("Barcode Startswith " + Barcode[-13] + Barcode[-12] + Barcode[-11] + Barcode[-10])
        print("0000 Barcode False")
        return False
    else:
        EndInt = str(Barcode)[-1]
        Sum = 0
        for x in range(1, 13):
            if int(x / 2) == x / 2:
                print("a = 3")
                a = 3
            else:
                print("a = 1")
                a = 1
            Sum = Sum + int(Barcode[-13 + x]) * a
            print("Sum = " + str(Sum) + " + " + str(Barcode[-13 + x]) + ") * " + str(x))
        print("Sum " + str(Sum))
        End = str(10 - int(str(Sum)[-1]))[-1]
        print("End " + str(End))
        print("EndInt " + str(EndInt))
        if str(End) == str(EndInt):
            print("Barcode is True")
            return True
        else:
            print("Barcode is False")
            return True  ##False # Test geht nur wenn barcode von mie ist


def IDToBarcode(ID):
    print("ID To Barcode")
    Barcode = "123456" + str(ID)
    if len(str(ID)) == 6:
        print("Barcode " + str(Barcode))
        Sum = 0
        for x in range(1, 13):
            if int(x / 2) == x / 2:
                print("a = 3")
                a = 3
            else:
                print("a = 1")
                a = 1
            Sum = Sum + int(Barcode[-13 + x]) * a
        print("Sum = " + str(Sum) + " + " + str(Barcode[-13 + x]) + " * " + str(x))
        print("Sum " + str(Sum))
        End = str(10 - int(str(Sum)[-1]))[-1]
        Barcode = str(Barcode) + str(End)
        print("Barcode " + str(Barcode))
    return str(Barcode)


def PrintBarcode(IP, ID, Barcode, Name, Price):
    print("Barcode")

    ID = str(ID)
    Barcode = str(Barcode)
    Name = str(Name)
    Price = str(Price) + " Euro"

    BarcodePos = "^FO140,5^BY2"
    BarcodeType = "^BEI,30,N,N"
    BarcodeString = "^FD" + Barcode + "^FS"
    Barcode = BarcodePos + BarcodeType + BarcodeString

    IDPos = "^FO120,30^BY2"
    IDText = "^ACB^FD" + ID + "^FS"  # ^AOB^FD
    ID = IDPos + IDText

    MaxStringLen = 15
    if len(Name) < MaxStringLen:
        NamePos = "^FO150,70^BY1"
        NameText = "^ACN^FD" + Name + "^FS"
        Name = NamePos + NameText
    else:
        Name1 = Name[0:MaxStringLen]
        Name2 = Name[MaxStringLen:len(Name)]
        NamePos1 = "^FO150,70^BY1"
        NameText1 = "^ACN^FD" + Name1 + "^FS"
        NamePos2 = "^FO150,100^BY1"
        NameText2 = "^ACN^FD" + Name2 + "^FS"
        Name = NamePos1 + NameText1 + NamePos2 + NameText2

    PricePos = "^FO160,40^BY1"
    PriceText = "^ACN^FD" + Price + "^FS"
    Price = PricePos + PriceText

    zpl = "^XA" + Barcode + ID + Name + Price + "^XZ"
    if TCP_IP == "CUPS":
        open("DATA/PRINT", "w").write(zpl)
        os.system("lpr -o raw DATA/PRINT")
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytes(zpl, "utf-8"))
        s.close()


def PrintLocation(Location):
    Location = str(Location)

    BarcodePos = "^FO150,10^BY1"
    BarcodeType = "^B3,Y,40,N,N"
    BarcodeString = "^FD" + Location + "^FS"
    Barcode = BarcodePos + BarcodeType + BarcodeString

    StringPos = "^FO150,70^BY3"
    StringText = "^AFD^FD" + Location + "^FS"
    String = StringPos + StringText

    zpl = "^XA" + Barcode + String + "^XZ"

    if TCP_IP == "CUPS":
        open("DATA/PRINT", "w").write(zpl)
        os.system("lpr -o raw DATA/PRINT")
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytes(zpl, "utf-8"))
        s.close()


