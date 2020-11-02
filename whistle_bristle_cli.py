import argparse
import os
from utils.key_combination import check_key
from main import emergency_erase


def check_path(string):
    '''
    Check if the string path is file of directory
    '''
    # Checking with argparse.FileType() ?
    if os.path.isdir(string) or os.path.isfile(string):
        if string[-1] != '/' and os.path.isdir(string):
            string += '/'
        return string
    else:
        raise ValueError(string + ' is not a directory or regular file.')


def create_parser():
    # TODO: Set description for a parser

    desc = ''
    keycombo_help = "Key combination to start erase ( surround with '' )"
    files_help = 'Files and dirs you want to be deleted after pressing hotkey'

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('files',
                        nargs='+',
                        type=check_path,
                        help=files_help
                        )

    parser.add_argument('-k', "--key", '--keycombo',
                        type=check_key,
                        default='<ctrl>+<alt>+e',
                        help=keycombo_help
                        )
    return parser


def create_emergency_eraser(files, key):
    # print(f'Files: {files} | Key: {key}')
    ee = emergency_erase.EmergencyErase()

    pass


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    create_emergency_eraser(args.files, args.key)
