import argparse
import os
import sys
import whistle_bristle
from whistle_bristle.emergency_erase import EmergencyErase
from whistle_bristle.utils.key_combination import check_key
from whistle_bristle.utils.checkers import check_path, check_path_and_priority


def create_parser():
    # TODO: Set description for a parser

    desc = ''
    keycombo_help = "Key combination to start erase ( surround with '' )"
    files_help = 'Files and dirs you want to be deleted after pressing hotkey'
    files_priority_help = 'Files and dirs you want to be deleted after pressing hotkey with priority of deleting ( syntax: "path_to_file_or_dir@priority_number" )'
    files_delete_help = 'Deletes files from database'
    changing_priority_help = 'Changing priority of deleting files "filename@priority"'

    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers(dest='cmd_type')

    bristle_parser = subparsers.add_parser('bristle')
    bristle_actions = bristle_parser.add_mutually_exclusive_group()

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

    config_parser = subparsers.add_parser('config')
    config_actions = config_parser.add_mutually_exclusive_group()
    config_actions.add_argument('-i', '--info',
                                action='store_true',
                                default=False,
                                help='Show information about config file')
    config_actions.add_argument('-db', '--pathtodb',
                                action='store_true',
                                default=False,
                                help='Show files database path')

    whistle_parser = subparsers.add_parser('whistle')
    whistle_parser.add_argument('-k', '--keycombo',
                                type=check_key,
                                default='<ctrl>+<alt>+b',
                                help=keycombo_help
                                )
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    ee = EmergencyErase()
    if ee.is_blank_config():
        ee.set_default_config()

    # TODO if only command name print help

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
        breakpoint()
        ee.start_listener()
