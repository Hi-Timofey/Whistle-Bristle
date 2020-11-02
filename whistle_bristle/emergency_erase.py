import daemon
from whistle_bristle.db import files


class EmergencyErase:
    def __init__(self, path_to_db):
        self.db = files.Files(path_to_db)
