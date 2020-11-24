# Whistle & Bristle

Program for "panic" situations which will delete important files when you press key combination.

### Usage

## Installation

First of all you need [Python3](https://www.python.org/) on your system with this libs:

  - Pynput
  - Daemon
  - PyQt5 ( if using GUI)
All dependencies are in requirements.txt

For installation you need to run this command in your terminal:
> $ pip install -r requitements.txt

> $ python3 wb_cli.py -h ( for CLI version )

> $ python3 wb_qt.py ( for GUI version )

### Using in code

You can use library for building your own eraser via EmergencyErase class

#### Example of code

    from whistle_bristle import EmergencyErase
    ee = EmergencyErase()
    ee.set_blank_config()
    ee.load_database(create_if_no=True)
    ee.add_files_only('/home/user', '/var', '/etc')
    ee.set_keycombo(keycombo='Ctrl+Alt+d')
    ee.start_listener(daemonize=True)

## Author

This if program of [Timofey Katkov](https://github.com/Hi-Timofey), 2 course of Yandex Lyceum. 
