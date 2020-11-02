# -*- coding: utf-8 -*-
import sqlite3 as sql

DEFAULT_PATH = 'whistle_bristle/whistle_bristle/db/'


class FilesDB():

    def __init__(self, path=DEFAULT_PATH):
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

    def add_files_only(self, files):
        for f in files:
            self.cur.execute(f"insert into files values('{f}', 4)")
        self.db_connect.commit()

    def add_files_with_priority(self, files_with_priority):
        for f in files_with_priority:
            path, priority = f
            self.cur.execute(f"insert into files values('{path}', {priority})")

        self.db_connect.commit()

    def delete_files(self, files):
        for f in files:
            query = f"delete from files where path like '{f}'"
            self.cur.execute(query)

        # TODO: real commiting
        self.db_connect.commit()

    def change_priority_of_file(self, files):
        for f in files:
            path, priority = f
            query = f"update files set priority = {priority} where path like '{path}'"
            self.cur.execute(query)

        # TODO: real commiting
        self.db_connect.commit()



if __name__ == '__main__':
    db = FilesDB(DEFAULT_PATH + 'files.db')
    db.start()
    print(*db.get_all_data())
    db.stop()
