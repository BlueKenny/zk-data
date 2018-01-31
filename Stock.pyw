#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import libs.send


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

            IDsInStock = libs.send.SendeSucheStock(text_suche, "", "")[:-3].split("<K>")
            if "0" in IDsInStock: del IDsInStock[IDsInStock.index("0")]

            print("IDsInStock: " + str(IDsInStock))

            for x in sorted(range(0, 50), reverse=True):
                self.model.removeRow(x)

            for id in IDsInStock:
                data = libs.send.StockGetArtInfo(["Anzahl", "Lieferant", "Name", "Artikel", "Ort", "PreisVK"], id).split(" | ")
                Anzahl = data[1]
                Lieferant = data[2].title()
                Name = data[3]
                Artikel = data[4].upper()
                Ort = data[5].upper()
                PreisVK = data[6]


                #ListItem = QListWidgetItem(self.Suche_List)
                #ListItem.setText(str(id))

                Items = []
                Items.append(QStandardItem(str(Name)))
                Items.append(QStandardItem(str(Artikel)))
                Items.append(QStandardItem(str(Lieferant)))
                Items.append(QStandardItem(str(Ort)))
                Items.append(QStandardItem(str(PreisVK)))
                Items.append(QStandardItem(str(Anzahl)))

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
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.Stretch)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.Suche_Entry.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Stock()
    sys.exit(app.exec_())