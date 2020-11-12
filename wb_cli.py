#!/usr/bin/env python3
import argparse
import os
import sys
import whistle_bristle
from whistle_bristle.emergency_erase import EmergencyErase
from whistle_bristle.utils.key_combination import check_key
from whistle_bristle.utils.checkers import check_path, check_path_and_priority

version = '1.0'


def create_parser():
    # TODO: Add translator

    prog = "Whistle&Bristle"
    wb_desc = "This program can help you in emergency situation by deleting all \
        files that you don't want to be on your computer when someone \nwill \
        take control over it. Firstly, you set some configuration. Secondly,\
        set 'bristle' files, which will be deleted. Finally, start 'whistle'\
        and when you press key combination, files will be deleted."
    epilog = '(c) Timofey 2020. The author of the program, as always, \
        assumes no responsibility for anything.'
    bristle_help = 'Manipulating with important files database.'
    whistle_help = 'Start listening for key combination you choose and\
        deletes files when it presse.'
    config_help = 'Configure the program (like database path and etc).'
    keycombo_help = "Key combination to start erase ( surround with '' )"
    files_help = 'Files and dirs you want to be deleted after pressing hotkey'
    files_priority_help = 'Files and dirs you want to be deleted after \
        pressing hotkey with priority of deleting ( syntax: \
        "filename@priority" )'
    files_delete_help = 'Deletes files from database'
    changing_priority_help = 'Changing priority of deleting \
        files "filename@priority"'
    list_help = 'List all important files and dirs'
    deleteall_help = 'Delete all files and dirs from database'

    parser = argparse.ArgumentParser(
        prog=prog, description=wb_desc, epilog=epilog)
    parser.add_argument('--version','-v',
                        action='version',
                        help='Show program version',
                        version=f'%(prog)s {version}')
    subparsers = parser.add_subparsers(
        dest='cmd_type', title='Possible commands')

    bristle_parser = subparsers.add_parser(
        'bristle', description=bristle_help, help=bristle_help)
    bristle_actions = bristle_parser.add_mutually_exclusive_group()

    bristle_actions.add_argument('-fo', '--filesonly',
                                 nargs='+',
                                 type=check_path,
                                 default=False,
                                 help=files_help,
                                 metavar='filename'
                                 )
    bristle_actions.add_argument('-da', '--deleteall',
                                 action='store_true',
                                 help=deleteall_help,
                                 default=False)
    bristle_actions.add_argument('-l', '--listfiles',
                                 action='store_true',
                                 help=list_help,
                                 default=False)
    bristle_actions.add_argument('-fp', '--filespriority',
                                 nargs='+',
                                 metavar='filename@4',
                                 type=check_path_and_priority,
                                 default=False,
                                 help=files_priority_help
                                 )
    bristle_actions.add_argument('-d', '--delete',
                                 nargs='+',
                                 metavar='filename',
                                 type=check_path,
                                 default=False,
                                 help=files_delete_help
                                 )
    bristle_actions.add_argument('-cp', '--changepriority',
                                 nargs='+',
                                 metavar='filename@4',
                                 type=check_path_and_priority,
                                 default=False,
                                 help=changing_priority_help
                                 )

    config_parser = subparsers.add_parser(
        'config', description=config_help, help=config_help)
    config_actions = config_parser.add_mutually_exclusive_group()
    config_actions.add_argument('-i', '--info',
                                action='store_true',
                                default=False,
                                help='Show information about config file')
    config_actions.add_argument('-db', '--pathtodb',
                                action='store_true',
                                default=False,
                                help='Show files database path')

    whistle_parser = subparsers.add_parser(
        'whistle', description=whistle_help, help=whistle_help)
    whistle_parser.add_argument('-k', '--keycombo',
                                metavar='<key>+<Combination>+letter',
                                type=check_key,
                                default='<ctrl>+<alt>+e',
                                help=keycombo_help
                                )
    whistle_parser.add_argument('-d', '--daemon',
                                action='store_true',
                                default=False,
                                help='Start listening hotkey in backgroud (daemon prosecc)')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    ee = EmergencyErase()
    if ee.is_blank_config():
        ee.set_default_config()

    if args.cmd_type == 'config':
        if args.pathtodb:
            path_to_db = ee.get_database_path()
            print(
                f'Path to database: {path_to_db}')
        if args.info:
            print(ee.get_database_info())

    elif args.cmd_type == 'bristle':
        ee.load_database(create_if_no=True)


        if args.delete:
            ee.delete_files(args.delete)

        if args.changepriority:
            ee.change_priority_of_file(args.changepriority)

        if args.filesonly:
            ee.add_files_only(args.filesonly)

        if args.filespriority:
            ee.add_files_with_priority(args.filespriority)

        if args.deleteall:
            ee.delete_all_files()

        if args.listfiles:
            data = ee.get_all_data()
            if len(data) >= 1:

                for d in data:
                    path, p = d
                    print(f'| Priority: {p} * Path to file: {path} \t')
            else:
                print('There are no files in database to erase!')
    elif args.cmd_type == 'whistle':

        # TODO Make logging options
        # TODO Rewrite this to factory pattern (because I want)

        ee.load_database()

        ee.set_priorities(True)
        ee.set_keycombo(keycombo=args.keycombo)

        #TODO Test
        daemonie = False# args.daemon
        ee.start_listener(daemonize=daemonie)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
