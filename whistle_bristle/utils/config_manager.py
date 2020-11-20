from .checkers import check_cfg_file
import os


class ConfigError(Exception):
    pass

# TODO Make syntax checker for config file
class ConfigManager():

    DATABASE_PATH = 'database_path'

    def __init__(self, project_dir, cfgfile_path=None):
        self.project_dir = project_dir
        self.cfgfile_name = 'config.txt'
        if cfgfile_path is None:
            self.cfgfile_path = self.project_dir + self.cfgfile_name
        else:
            self.cfgfile_path = cfgfile_path
        self._init_cfg_file()

        self.DEFAULT_CONFIG = {
            'database_path': f'{self.project_dir}whistle_bristle/db/files.sqlite'
            }

    def erase(self):
        os.remove(self.cfgfile_path)
        self.project_dir = None

    def get_info(self):
        return f'Config file "{self.cfgfile_name}":\n\tIs empty: {self.is_blank_cfg()}\n\tPath to: {self.cfgfile_path}'

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
        '''Setting config file to the default state'''

        with open(self.cfgfile_path, 'w') as cfgfile:
            for cfg in self.DEFAULT_CONFIG:
                cfgfile.write(f'{cfg}={self.DEFAULT_CONFIG[cfg]}' + '\n')


    def set_cfg_value(self, key, value):
        '''Set some value to config'''
        key = key.lower().strip().replace('\n','').replace('\t','')
        value = value.strip().replace('\n','').replace('\t','')
        if key not in self.DEFAULT_CONFIG.keys():
            raise ValueError('No such key in configuration of the app')

        print('---debug---\n')

        with open(self.cfgfile_path, 'r') as cfgfile:
            config = cfgfile.readlines()
            for line in config:
                if key in line:
                    del config[config.index(line)]

        with open(self.cfgfile_path, 'w') as cfgfile:
            for line in config:
                cfgfile.write(line)
            cfgfile.write(f'{key}={value}' + '\n')

        print('---end---\n')


    def get_cfg_value(self, key):
        '''Get some value from config'''

        with open(self.cfgfile_path, 'r') as cfgfile:
            cfg = cfgfile.readlines()
            for line in cfg:
                l = line.strip()
                if l[0] != '#' and '=' in l:
                    name, value = l.split('=')
                    if name == key:
                        return value
