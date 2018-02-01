#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

if os.path.exists("/home/phablet"): import send
else: import libs.send

class Stock(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle('Stock')

        grid = QGridLayout()
        grid.setSpacing(10)

        self.Suche_Entry = QLineEdit(self)
        self.Suche_Entry.textChanged.connect(self.startSuche)

        #self.Suche_List = QListWidget(self)
        self.Suche_Table = QTableView(self)
        self.Suche_Table.setSelectionBehavior(QTableView.SelectRows)
        self.model = QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.model.setHorizontalHeaderLabels(['Name', 'Artikel', 'Lieferant', "Ort", "Preis", "Anzahl"])
        self.Suche_Table.setModel(self.model)  # SETTING THE MODEL
        # self.doubleClicked.connect(self.select_index)

        grid.addWidget(self.Suche_Entry, 0, 0, 1, 2)
        #grid.addWidget(self.Suche_List, 1, 0)
        grid.addWidget(self.Suche_Table, 1, 1)

        self.setLayout(grid)
        self.setGeometry(500, 500, 800, 800)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def startSuche(self):
        print("startSuche")
        text_suche = self.Suche_Entry.text()
        if not text_suche == "":
            print("text_suche: " + text_suche)

            IDsInStock = libs.send.SucheStock(text_suche, "", "")[:-3].split("<K>")
            if "0" in IDsInStock: del IDsInStock[IDsInStock.index("0")]

            print("IDsInStock: " + str(IDsInStock))

            for x in sorted(range(0, 50), reverse=True):
                self.model.removeRow(x)

            for id in IDsInStock:
                TimeStamp = id.split("|")[1]
                id = id.split("|")[0]

                # If ID is key in Daten
                # Test TimeStamp with Server

                data = libs.send.StockGetArtInfo(["Name", "Artikel", "Lieferant", "Ort", "PreisVK", "Anzahl"], id).split(" | ")
                Name = data[1]
                Artikel = data[2].upper()
                Lieferant = data[3].title()
                Ort = data[4].upper()
                PreisVK = data[5]
                Anzahl = data[6]


                #ListItem = QListWidgetItem(self.Suche_List)
                #ListItem.setText(str(id))

                Items = []
                for each in data:
                    if not str(each) == str(id):
                        thisItem = QStandardItem(str(each))
                        #thisItem.setFlags(Qt.ItemIsEnabled)
                        Items.append(thisItem)

                #Items.append(QStandardItem(str(Name)))
                #Items.append(QStandardItem(str(Artikel)))
                #Items.append(QStandardItem(str(Lieferant)))
                #Items.append(QStandardItem(str(Ort)))
                #Items.append(QStandardItem(str(PreisVK)))
                #Items.append(QStandardItem(str(Anzahl)))

                #if Anzahl == 0:
                #    BildPfad = "DATA/Bilder/Stock/" + Lieferant + ".0.jpg"
                #    if not os.path.exists(BildPfad):
                #        BildPfad = "DATA/Bilder/Stock/NoImage.0.jpg"
                #    ListItem.setIcon(QIcon(BildPfad))
                #else:
                #    BildPfad = "DATA/Bilder/Stock/" + Lieferant + ".Stock.jpg"
                #    if not os.path.exists(BildPfad):
                #        BildPfad = "DATA/Bilder/Stock/NoImage.Stock.jpg"
                #    ListItem.setIcon(QIcon(BildPfad))
                self.model.appendRow(Items)
            self.model.setVerticalHeaderLabels(IDsInStock)
            header = self.Suche_Table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.Stretch)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.Suche_Entry.clear()



if __name__ == '__main__':
    Daten = {}
    app = QApplication(sys.argv)
    ex = Stock()
    sys.exit(app.exec_())
