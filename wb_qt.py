#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class WhistleBristleMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('qt/main.ui', self)  # Загружаем дизайн



if __name__ == '__main__':
    app = QApplication(sys.argv)
    wb = WhistleBristleMainWindow()
    wb.show()
    sys.exit(app.exec_())
