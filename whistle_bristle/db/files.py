# -*- coding: utf-8 -*-
import sqlite3 as sql


class FilesDB():

    def __init__(self, path='files.db'):
        self.path = path
        self.cur = None
        self.db_connect = None

    def start(self):
        self.db_connect = sql.connect(self.path)
        self.cur = self.db_connect.cursor()

    def stop(self):
        self.cur = None
        self.db_connect.close()

    def get_all_paths(self):
        return self.cur.execute('select distinct path from files').fetchall()

    def get_all_data(self, sorted=True):
        if sorted:
            return self.cur.execute('''select distinct * from files
                                    order by priority asc''').fetchall()
        else:
            return self.cur.execute('select distinct * from files').fetchall()


if __name__ == '__main__':
    db = FilesDB()
    db.start()
    print(*db.get_all_data())
    db.stop()
