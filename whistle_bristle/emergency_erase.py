import daemon
from whistle_bristle.db import files
from whistle_bristle.utils import key_combination


class EmergencyErase:
    def __init__(self, path_to_db=None, keycombo=None):
        if path_to_db is None:
            raise files.DBError('Please, pass path to "erasing database"')
        self.db = files.FilesDB(path_to_db)

        if keycombo is None:
            raise key_combination.KeyComboError(
                'Please, pass hotkey for erasing')
        self.keycombo = keycombo
        self.key_listener = key_combination.KeyCombinationListener(
            self.keycombo, lambda: print('get ready for deleting'), self.run)

    def start_listener(self):
        self.key_listener.start_listening()

    def run(self):
        print('emergecny circumstantion!')
        with open('somefile.txt', 'w') as f:
            pass
