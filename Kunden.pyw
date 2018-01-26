#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Suchen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kunden Suche")
        self.setGeometry(10, 10, 640, 480)

        btn_search = QPushButton("Suchen", self)
        btn_search.setToolTip("Suche Starten")
        btn_search.move(100, 70)
        btn_search.clicked.connect(self.func_btn_search)

        btn_change = QPushButton("Ändern", self)
        btn_change.setToolTip("Suche Starten")
        btn_change.move(300, 70)
        btn_change.clicked.connect(self.func_btn_change)

        self.show()

    @pyqtSlot()
    def func_btn_search(self):
        global NextFrame
        print("Start Suchen")
        self.close()
    def func_btn_change(self):
        global NextFrame
        print("yes")
        self.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Suchen()
    sys.exit(app.exec_())