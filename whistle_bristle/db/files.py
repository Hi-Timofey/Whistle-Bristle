# -*- coding: utf-8 -*-
import sqlite3 as sql
from os.path import isfile, getsize


class DBError(ValueError):
    pass


class FilesDB():

    def __init__(self, path=None, create_if_no=False):
        if path is None:
            raise ValueError('No path to db')
        if not FilesDB.isSQLite3(path):
            if not create_if_no:
                raise DBError('There are no sql database file')
        self.path = path
        self.cur = None
        self.db_connect = None
        if create_if_no and self.is_empty():
            self.create_default()

    def get_path(self):
        return self.path

    def create_default(self):
        '''Creates the default database with "Files" table'''
        self._start()
        query_table = '''
        CREATE TABLE "files" (
	"path"	text NOT NULL UNIQUE,
	"priority"	integer NOT NULL DEFAULT 4,
	PRIMARY KEY("path"));
        '''
        self.cur.execute(query_table)
        self.db_connect.commit()
        self._stop()

    def _start(self):
        self.db_connect = sql.connect(self.path)
        self.cur = self.db_connect.cursor()

    def _stop(self):
        self.cur = None
        self.db_connect.close()

    def isSQLite3(filename):
        if not isfile(filename):
            return False
        if getsize(filename) < 100:  # SQLite database file header is 100 bytes
            return False

        with open(filename, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == b'SQLite format 3\x00'

    def get_all_paths(self):
        self._start()

        respones = self.cur.execute(
            'select distinct path from files').fetchall()

        self._stop()
        return respones

    def get_all_data(self, priorities=True):
        self._start()

        if priorities:
            response = self.cur.execute('''select distinct * from files
                                    order by priority asc''').fetchall()
        else:
            response = self.cur.execute(
                'select distinct * from files').fetchall()

        self._stop()
        return response

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

        # TODO count deleted files
        for f in files:
            query = f"delete from files where path like '{f}'"
            self.cur.execute(query)

        self.db_connect.commit()

        self._stop()

    def delete_all_files(self):
        self._start()
        # TODO count deleted files

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

    # TODO Rename to is_empty_table
    def is_empty(self) -> bool:
        self._start()
        q = 'SELECT CASE WHEN EXISTS(SELECT 1 FROM files) THEN 0 ELSE 1 END AS IsEmpty;'
        response = bool(self.cur.execute(q).fetchone()[0])
        self._stop()
        return response

    def is_empty_base(self):
        pass
        self._start()
        q = 'SELECT object_id FROM sys.tables WHERE name = 'Artists';'
        response = bool(self.cur.execute(q).fetchone()[0])
        self._stop()
        # if lasjfklsdjf TODO
        return response


if __name__ == '__main__':
    pass
    # db = FilesDB()
    # db.start()
    # print(*db.get_all_data())
    # db.stop()
