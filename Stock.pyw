#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

if os.path.exists("/home/phablet"): import send
else: import libs.send


ThingsToShowInTable = ['name', 'artikel', 'lieferant', "ort", "preisvk", "anzahl"]
ThingsToShowAsHeader = ['Name', 'Artikel', 'Lieferant', "Ort", "Preis", "Anzahl"]

class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.center()
        self.setWindowTitle('Info')

        grid = QGridLayout()
        grid.setSpacing(10)


        self.setLayout(grid)
        self.setGeometry(220, 400, 900, 800)
        self.show()

class Stock(QWidget):#QWidget
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle('Stock')
        self.setWindowIcon(QIcon("DATA/icon.jpeg"))

        self.stacked_layout = QStackedWidget()
        self.stacked_layout.addWidget(Info())

        grid = QGridLayout()
        grid.setSpacing(10)

        self.Suche_Entry = QLineEdit(self)
        self.Suche_Entry.textChanged.connect(self.startSuche)

        self.Suche_Table = QTableView(self)
        self.Suche_Table.setSelectionBehavior(QTableView.SelectRows)
        self.model = QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.model.setHorizontalHeaderLabels(ThingsToShowAsHeader)
        self.Suche_Table.setModel(self.model)  # SETTING THE MODEL
        self.Suche_Table.doubleClicked.connect(self.ShowArtInfos)

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

    def ShowArtInfos(self):
        print("ShowInfoWindow")
        #self.hide()
        self.stacked_layout.setCurrentIndex(2)

    def startSuche(self):
        print("startSuche")
        text_suche = self.Suche_Entry.text()
        if not text_suche == "":
            print("text_suche: " + text_suche)

            IDsAndTime = libs.send.SearchArt({"suche":Suche, "ort":Ort, "lieferant":Lieferant})
            #if IDsAndTime == [""]: del IDsAndTime[0]

            print("IDsAndTime: " + str(IDsAndTime))

            for x in sorted(range(0, 50), reverse=True):
                self.model.removeRow(x)

            IDs = []
            for IDAndTime in IDsAndTime:
                id = IDAndTime.split("|")[0]
                TimeStampServer = str(IDAndTime.split("|")[1])

                TimeStampLocal = libs.send.GetArtLocal(str(id))["LastChange"]


                # Test TimeStamp with Server
                print("TimeStampLocal: " + str(TimeStampLocal))
                if TimeStampServer == TimeStampLocal:
                    print("Local Data")
                    data = libs.send.GetArtLocal(id)
                else:
                    print("Server Data")
                    data = libs.send.GetArtStock(id)
                print("data " + str(data))
                Items = []
                for each in ThingsToShowInTable:
                    thisItem = QStandardItem(str(data[each]))
                    thisItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    #thisItem.setFlags(Qt.ItemIsEnabled)
                    Items.append(thisItem)


                self.model.appendRow(Items)
            self.model.setVerticalHeaderLabels(IDs)
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
    app = QApplication(sys.argv)
    ex = Stock()
    sys.exit(app.exec_())
