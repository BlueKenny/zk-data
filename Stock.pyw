#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#need
#python3-qt5
#qt5
import sys
from PyQt5.QtCore import QObject, QUrl, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

def show(text):
    print(text)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  engine = QQmlApplicationEngine()
  engine.load('Stock.qml')
  win = engine.rootObjects()[0]
  win.textUpdated.connect(show)
  win.show()
  sys.exit(app.exec_())
