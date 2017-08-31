'''
Manage User Command Line Interface
'''
from argparse import ArgumentParser
from .core import run_command


def main():
    '''
    Main Program
    '''
    parser = ArgumentParser(prog='dtp', usage='%(prog)s <action> <name>')
    parser.add_argument('action', choices=['create',
                                           'destroy',
                                           'halt',
                                           'info',
                                           'list',
                                           'login',
                                           'pull',
                                           'push',
                                           'start',
                                           'status'],
                        help='action required')
    parser.add_argument('name', help='Name of resource to create, matching config file')
    parser.add_argument('--debug', '-d', '-D', action='store_true', help='Set log level to debug')
    args = parser.parse_args()
    run_command(args)

if __name__ == '__main__':
    main()
