import argparse
import os
import sys
import whistle_bristle
from whistle_bristle import emergency_erase
from whistle_bristle.utils.key_combination import check_key
from whistle_bristle.utils.checkers import check_path, check_path_and_priority
from whistle_bristle.utils.config_manager import ConfigManager
from whistle_bristle.db import files

# PATH TO THE PROJECT
project_wd = os.path.dirname(os.path.abspath(sys.argv[0])) + '/'

# Creates ConfigManager file
cfg_manager = ConfigManager(project_wd)
if cfg_manager.is_blank_cfg():
    answer = str(input('Do you want to set default config?[Y/n]:')).strip()
    if answer.lower() == 'y':
        cfg_manager.set_default()

input('STOP IT')


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

    bristle_actions.add_argument('-da', '--deleteall',
                                 action='store_true',
                                 default=False)

    bristle_actions.add_argument('-l', '--listfiles',
                                 action='store_true',
                                 default=False)

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

    if args.deleteall:
        db.delete_all_files()

    if args.listfiles:
        data = db.get_all_data()
        if len(data) >= 1:

            for d in data:
                path, p = d
                print(f'| Priority: {p} * Path to file: {path} \t')
        else:
            print('There are no files in database to erase!')


if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.cmd_type == 'bristle':
        bristle_working(args)
    elif args.cmd_type == 'whistle':
        whistle_working(args)
