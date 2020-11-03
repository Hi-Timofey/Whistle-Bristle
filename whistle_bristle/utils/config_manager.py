from .checkers import check_cfg_file
import os


class ConfigError(Exception):
    pass


# TODO Make syntax checher for config file
class ConfigManager():

    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.cfgfile_name = 'config.txt'
        self.cfgfile_path = self.project_dir + self.cfgfile_name
        self._init_cfg_file()

    def _init_cfg_file(self):
        '''Creates config file if it is not exists.'''

        if not check_cfg_file(self.cfgfile_path):
            with open(self.cfgfile_path, 'w') as cfgfile:
                pass

    def is_blank_cfg(self):
        if check_cfg_file(self.cfgfile_path):
            if os.path.getsize(self.cfgfile_path) > 0:
                return False
        return True

    def set_default(self):
        print(self.project_dir)

        # with open(self.cfgfile_path, 'w') as cfgfile:
        #     cfgfile.write(f'database_path = {self}' + '\n')
