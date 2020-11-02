import argparse
import os
import sys
import whistle_bristle
from whistle_bristle import emergency_erase
from whistle_bristle.utils.key_combination import check_key
from whistle_bristle.db import files


def check_path(string):
    '''
    Check if the string path is file of directory
    '''

    if os.path.isdir(string) or os.path.isfile(string):
        string = os.path.abspath(string)
        if string[-1] != '/' and os.path.isdir(string):
            string += '/'
        return string
    else:
        raise ValueError(string + ' is not a directory or regular file.')


def check_path_and_priority(string):
    '''
    Check if the string path is file of directory
    '''

    try:
        path, priority = string.split('@')
    except ValueError:
        raise ValueError(
            f'"{string}" has incorrect syntax ( example: "file.txt@4" )')

    if os.path.isdir(path) or os.path.isfile(path):
        path = os.path.abspath(path)
        if path[-1] != '/' and os.path.isdir(path):
            path += '/'
        return (path, int(priority),)
    else:
        raise ValueError(path + ' is not a directory or regular file.')


def create_parser():
    # TODO: Set description for a parser

    desc = ''
    keycombo_help = "Key combination to start erase ( surround with '' )"
    files_help = 'Files and dirs you want to be deleted after pressing hotkey'
    files_priority_help = 'Files and dirs you want to be deleted after pressing hotkey with priority of deleting ( syntax: "path_to_file_or_dir@priority_number" )'
    files_delete_help = 'Deletes files from database'
    changing_priority_help = 'Changing priority of deleting files'

    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers(dest='cmd_type')

    bristle_parser = subparsers.add_parser('bristle')
    bristle_actions = bristle_parser.add_mutually_exclusive_group()

    # whistle_parser = subparsers.add_parser('whistle')

    bristle_actions.add_argument('-fo', '--filesonly',
                                 nargs='+',
                                 type=check_path,
                                 default=False,
                                 help=files_help
                                 )

    bristle_actions.add_argument('-fp', '--filespriority',
                                 nargs='+',
                                 type=check_path_and_priority,
                                 default=False,
                                 help=files_priority_help
                                 )
    bristle_actions.add_argument('-d', '--delete',
                                 nargs='+',
                                 type=check_path,
                                 default=False,
                                 help=files_delete_help
                                 )
    bristle_actions.add_argument('-cp', '--changepriority',
                                 nargs='+',
                                 type=check_path_and_priority,
                                 default=False,
                                 help=changing_priority_help
                                 )

    # whistle_parser.add_argument('-k', "--key", '--keycombo',
    #                     type=check_key,
    #                     default='<ctrl>+<alt>+e',
    #                     help=keycombo_help
    #                     )
    return parser


def whistle_working(args):
    pass


def bristle_working(args):
    # TODO: Not correct selecting path for database
    path = '/home/katok/combat/python_workspace/whistle_bristle/whistle_bristle/db/files.db'
    db = files.FilesDB(path)

    if args.delete:
        db.delete_files(args.delete)

    if args.changepriority:
        db.change_priority_of_file(args.changepriority)

    if args.filesonly:
        db.add_files_only(args.filesonly)

    if args.filespriority:
        db.add_files_with_priority(args.filespriority)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.cmd_type == 'bristle':
        bristle_working(args)
    elif args.cmd_type == 'whistle':
        whistle_working(args)
