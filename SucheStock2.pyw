#!/usr/bin/env python3
from BlueFunc import *
from debug import Debug
import os
import send


#python3-pyqt5 .qtquick
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QLineEdit, QPushButton, QComboBox, QListWidget
from PyQt5.QtCore import QSize, QRect   


def Suche(btn):
	Debug("Suche")
	liste.clear()	

	AntwortList=send.SendeSucheStock(entrySuche.text().replace(" ", ""), entryOrt.text().upper(), entryLieferant.text().lower())

	
	for IDs in AntwortList.split("<K>"):
		if not IDs == "":
			Linie = str(IDs).rstrip()
			
			Linie = send.StockGetArtInfo("(zkz)Name(zkz)Ort(zkz)PreisVK", IDs)

			liste.addItem(Linie)



app = QtWidgets.QApplication(sys.argv)
frame = QWidget()

frame.setWindowTitle("Stock Suche") 
frame.setGeometry(300, 300, 350, 300)

grid = QGridLayout(frame)
#grid.setSpacing(10)

frame.setLayout(grid)

labelSuche = QLabel("Suche") 
grid.addWidget(labelSuche, 1, 0)

entrySuche = QLineEdit("")
grid.addWidget(entrySuche, 1, 1)

labelOrt = QLabel("Ort") 
grid.addWidget(labelOrt, 2, 0)

entryOrt = QLineEdit("")
grid.addWidget(entryOrt, 2, 1)

labelLieferant = QLabel("Lieferant") 
grid.addWidget(labelLieferant, 3, 0)

entryLieferant = QLineEdit("")
grid.addWidget(entryLieferant, 3, 1)

buttonSuche = QPushButton("Suchen")
grid.addWidget(buttonSuche, 4, 0, 1, 2)
buttonSuche.clicked.connect(Suche)
buttonSuche.setToolTip("Suche Starten")

liste = QListWidget()
grid.addWidget(liste, 5, 0, 10, 2)

frame.show()
sys.exit(app.exec_())
