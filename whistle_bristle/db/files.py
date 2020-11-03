# -*- coding: utf-8 -*-
import sqlite3 as sql

DEFAULT_PATH = 'whistle_bristle/whistle_bristle/db/files.db'


class FilesDB():

    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.cur = None
        self.db_connect = None

    def _start(self):
        self.db_connect = sql.connect(self.path)
        self.cur = self.db_connect.cursor()

    def _stop(self):
        self.cur = None
        self.db_connect.close()

    def get_all_paths(self):
        self._start()

        return self.cur.execute('select distinct path from files').fetchall()

        self.stop()

    def get_all_data(self, sorted=True):
        self._start()

        if sorted:
            return self.cur.execute('''select distinct * from files
                                    order by priority asc''').fetchall()
        else:
            return self.cur.execute('select distinct * from files').fetchall()

        self._stop()

    def add_files_only(self, files):
        self._start()

        for f in files:
            self.cur.execute(f"insert into files values('{f}', 4)")
        self.db_connect.commit()

        self._stop()

    def add_files_with_priority(self, files_with_priority):
        self._start()

        for f in files_with_priority:
            path, priority = f
            self.cur.execute(f"insert into files values('{path}', {priority})")

        self.db_connect.commit()

        self._stop()

    def delete_files(self, files):
        self._start()

        for f in files:
            query = f"delete from files where path like '{f}'"
            self.cur.execute(query)

        # TODO: real commiting
        self.db_connect.commit()

        self._stop()

    def delete_all_files(self):
        self._start()

        query = f"delete from files"
        self.cur.execute(query)

        # TODO: real commiting
        self.db_connect.commit()

        self._stop()

    def change_priority_of_file(self, files):
        self._start()

        for f in files:
            path, priority = f
            query = f"update files set priority = {priority} where path like '{path}'"
            self.cur.execute(query)

        # TODO: real commiting
        self.db_connect.commit()

        self._stop()


if __name__ == '__main__':
    db = FilesDB(DEFAULT_PATH)
    db.start()
    print(*db.get_all_data())
    db.stop()
