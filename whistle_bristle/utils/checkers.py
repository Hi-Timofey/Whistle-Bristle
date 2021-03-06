import os


def check_cfg_file(cfgfile_path):
    '''Check if config file exists or not'''

    return os.path.isfile(cfgfile_path)


def check_path(string):
    '''

    '''

    path = os.path.expanduser(string)
    if os.path.isdir(path) or os.path.isfile(path):
        path = os.path.abspath(path)
        if path[-1] != '/' and os.path.isdir(path):
            path += '/'
        return path
    else:
        raise ValueError(path + ' is not a directory or regular file.')


def check_path_and_priority(string):
    '''
    Check if the string path is file of directory
    '''

    try:
        path, priority = string.split('@')
    except ValueError:
        raise ValueError(
            f'"{string}" has incorrect syntax ( example: "file.txt@4" )')

    if not 1 <= int(priority) <= 7:
        raise ValueError('Incorrect priority number (must be from 1 to 7)')
    path = os.path.expanduser(path)
    if os.path.isdir(path) or os.path.isfile(path):
        path = os.path.abspath(path)
        if path[-1] != '/' and os.path.isdir(path):
            path += '/'
        return (path, int(priority),)
    else:
        raise ValueError(path + ' is not a directory or regular file.')
