#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTableWidgetItem
import whistle_bristle
from whistle_bristle.emergency_erase import EmergencyErase


class WhistleBristleMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('qt/main.ui', self)  # Загружаем дизайн
        self.main()

    def main(self):
        self.onCreate()
        self.tableView()

    def onCreate(self):

        self.tableWidget.setHorizontalHeaderLabels('Path Priority'.split())

        self.ee = EmergencyErase()
        if self.ee.is_blank_config():
            self.ee.set_default_config()
        self.path_to_cur_db.setText(self.ee.get_database_path())

    def tableView(self):
        self.ee.load_database(create_if_no=True)
        self.refreshBtn.clicked.connect(self.refresh_result)

        self.tableWidget.cellChanged.connect(self.item_changed)
        self.saveBtn.clicked.connect(self.save_results)
        self.addBtn.clicked.connect(self.add_result)

    #----
    def save_results(self):
        print('save')
        self.statusBar().showMessage('Saving.')

    def item_changed(self):
        print('item')
        self.statusBar().showMessage('Item changed.')
    #----

    def add_result(self):
        print('add')
        self.tableWidget.insertRow(1)

    def refresh_result(self):
        result = self.ee.get_all_data()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Database is empty.')
            return
        else:
            self.statusBar().showMessage('Database is refreshing...')

        self.tableWidget.setColumnCount(len(result[0]))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


    def item_changed(self):
        pass

    def save_results(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wb = WhistleBristleMainWindow()
    wb.show()
    sys.exit(app.exec_())
