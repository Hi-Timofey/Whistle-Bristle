import shutil
import os
import sys
from whistle_bristle.utils.config_manager import *
from whistle_bristle.db.files import *
from whistle_bristle.utils.key_combination import *
# import daemon


class EEBaseError(Exception):
    pass


class EEDataBaseError(EEBaseError):
    pass


class EmergencyErase:
    def __init__(self, config_path=None):
        self.project_wd = os.path.dirname(os.path.abspath(sys.argv[0])) + '/'
        self.config = ConfigManager(self.project_wd, config_path)

    def is_blank_config(self):
        return self.config.is_blank_cfg()

    def set_default_config(self):
        self.config.set_default()

    def set_config_settings(self, key, value):
        # TODO need testing
        self.config.set_cfg_value(key, value)

    def get_database_path(self):
        return self.config.get_cfg_value(ConfigManager.DATABASE_PATH)

    def get_database_info(self):
        return self.config.get_info()

    def load_database(self, create_if_no=False):
        path_to_db = self.get_database_path()
        db = FilesDB(path_to_db, create_if_no=create_if_no)
        self.database = db

    def _check_db_path(self):
        if self.get_database_path() != self.database.get_path():
            raise EEDataBaseError(
                'Config path to database not equals with loaded database')
        return True

    def delete_all_files(self):
        if self._check_db_path():
            return self.database.delete_all_files()

    def delete_files(self, files):
        if self._check_db_path():
            return self.database.delete_files(files)

    def change_priority_of_file(self, changepriority):
        if self._check_db_path():
            self.database.change_priority_of_file(changepriority)

    def add_files_only(self, filesonly):
        if self._check_db_path():
            self.database.add_files_only(filesonly)

    def add_files_with_priority(self, filespriority):
        if self._check_db_path():
            self.database.add_files_with_priority(filespriority)

    def get_all_data(self):
        if self._check_db_path():
            return self.database.get_all_data()

    def set_keycombo(self, keycombo='<ctrl>+<alt>+e'):
        if keycombo is None:
            raise key_combination.KeyComboError(
                'Please, pass hotkey for erasing')
        self.keycombo = keycombo
        self.key_listener = KeyCombinationListener(
            self.keycombo, self._log, self.run)

    def _log(self):
        print('Key combo released')

    def start_listener(self):
        self.key_listener.start_listening()

        # TODO Can't run() if process is not running
        # (daemonize this or daemonize all the  script).
        while True:
            pass
        print('Process finished')

    def set_priorities(self, priorities):
        if priorities is not None:
            self.priorities = priorities
        else:
            raise ValueError('Not correct value')

    def get_priorities(self):
        if self.priorities is not None:
            return self.priorities
        else:
            raise TypeError('Null pointer exception')

    def run(self):
        self.files = self.database.get_all_data(
            priorities=self.get_priorities())

        print(f'{self.files}' + '\n\nStarting run...\n')

        for path, priority in self.files:
            # print(f'Path: {path} | Prio: {priority}')
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except BaseException as e:
                    print('Error while deleting file of db')
            if os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                except BaseException as e:
                    print(e)

        self.database.delete_all_files()
        print('Done')
