#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox, QFileDialog
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
        self.menuBar()
        self.onStart()

    def onStart(self):

        pass

    def menuBar(self):
        self.actionLoad_config_file.triggered.connect(self.load_config)
        self.actionSet_default_config.triggered.connect(
            self.ee.set_default_config)
        self.actionLoad_database.triggered.connect(self.load_db)
        self.actionExit.triggered.connect(exit)

    def load_config(*args):
        fname = QFileDialog.getOpenFileName(
            args[0], 'Load config file', '')[0].strip()
        print(fname, type(fname))
        try:
            args[0].ee.set_config_file(fname)
        except BaseException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You loaded wrong file")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Config error.")
            msg.exec_()

    # TODO
    def load_db(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Load database file', '')[0].strip()
        print(fname, type(fname))

        self.ee.set_config_value('database_path', fname)
        self.ee.load_database()
        self.path_to_cur_db.setText(
            'Path to db:' + self.ee.get_database_path())

    def onCreate(self):

        self.tableWidget.setHorizontalHeaderLabels('Path Priority'.split())

        self.ee = EmergencyErase()
        if self.ee.is_blank_config():
            self.ee.set_default_config()
        self.path_to_cur_db.setText(self.ee.get_database_path())

    def tableView(self):
        self.ee.load_database(create_if_no=True)
        self.refreshBtn.clicked.connect(self.refresh_result)
        self.tableWidget.setColumnWidth(0, 256)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.cellChanged.connect(self.item_changed)
        self.saveBtn.clicked.connect(self.save_results)
        self.addBtn.clicked.connect(self.add_result)

    def save_results(self):
        # TODO: Create radiobutton for not rewriting db
        self.statusBar().showMessage('Saving.')
        column = 0
        not_unique = []
        # rowCount() This property holds the number of rows in the table
        for row in range(self.tableWidget.rowCount()):
            # item(row, 0) Returns the item for the given row and column if one
            # has been set; otherwise returns nullptr.
            _item = self.tableWidget.item(row, column)
            if _item:
                path = self.tableWidget.item(row, column).text()
                prio = self.tableWidget.item(row, column+1).text()
                # print(f'row: {row}, column: {column}, item={item}')
                try:
                    if EmergencyErase.check_file_path_and_priority(
                            f'{path}@{prio}'):
                        try:
                            self.ee.add_files_with_priority((path, prio,))
                        except BaseException:
                            not_unique.append(path)
                except ValueError as e:
                    pass

        if len(not_unique) > 0:
            print(not_unique)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You entered not unique path")
            msg.setInformativeText(
                f'"{", ".join(not_unique)}" already in database')
            msg.setWindowTitle("Not unique path")
            msg.exec_()
        self.statusBar().showMessage('Changes writed, refresh table.')

    def item_changed(self, *coords):
        # print('item', self.tableWidget.item, coords)
        # self.statusBar().showMessage('Item changed.')
        row, col = coords
        item = self.tableWidget.item(row, col).text()
        if col == 0:
            try:
                if str(item) != ' ':
                    path = EmergencyErase.check_file_path(str(item))
            except BaseException as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You entered incorrect path")
                msg.setInformativeText(str(e)+' (dirs ends with "/")')
                msg.setWindowTitle("Incorrect value")
                msg.exec_()
                self.tableWidget.setItem(row, col, QTableWidgetItem(' '))
        elif col == 1:
            prio = self.tableWidget.item(row, col)
            try:
                assert 0 <= int(prio.text()) <= 7
            except BaseException as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You entered incorrect priority")
                msg.setInformativeText('Priority must be a number from 1 to 7')
                msg.setWindowTitle("Incorrect value")
                msg.exec_()
                self.tableWidget.setItem(row, col, QTableWidgetItem('4'))

    def add_result(self):
        self.tableWidget.insertRow(self.tableWidget.model().rowCount())

    def refresh_result(self):
        self.ee.load_database()
        result = self.ee.get_all_data()
        self.path_to_cur_db.setText(self.ee.get_database_path())
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
        self.statusBar().showMessage('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wb = WhistleBristleMainWindow()
    wb.show()
    sys.exit(app.exec_())
