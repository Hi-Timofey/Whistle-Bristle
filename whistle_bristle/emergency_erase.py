#import daemon
import shutil
import os
from whistle_bristle.db import files
from whistle_bristle.utils import key_combination


class EmergencyErase:
    def __init__(self, path_to_db=None, keycombo=None, priorities=True):
        self.priorities = priorities
        if path_to_db is None:
            raise files.DBError('Please, pass path to "erasing database"')
        self.db = files.FilesDB(path_to_db)

        if keycombo is None:
            raise key_combination.KeyComboError(
                'Please, pass hotkey for erasing')
        self.keycombo = keycombo
        self.key_listener = key_combination.KeyCombinationListener(
            self.keycombo, self._prepare_run, self.run)

    def start_listener(self):
        self.key_listener.start_listening()

        # TODO Can't run() if process is not running
        # (daemonize this or daemonize all the  script).
        while not self.db.is_empty():
            pass
        print('Process finished')

    def _prepare_run(self):
        self.files = self.db.get_all_data(priorities=self.priorities)

    def run(self):
        print(f'{self.files}' + '\n\nStarting run...\n')

        for path, priority in self.files:
            # print(f'Path: {path} | Prio: {priority}')
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except BaseException as e:
                    print(e)
            if os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                except BaseException as e:
                    print(e)


        self.db.delete_all_files()
        print('Done')
