'''
Manage instance status
'''
import json
import os
import sys
from .helper import verify_status_dir


class Status(object):
    '''
    Manage Status of all instances
    '''
    @staticmethod
    def create_status(status, status_file):
        '''
        Create new status file
        '''
        with open(status_file, 'w') as status_f:
            json.dump(status, status_f)

    @staticmethod
    def read_status(status_file):
        '''
        Read and return status from file
        '''
        with open(status_file) as status_f:
            status_data = json.load(status_f)
        return status_data

    @staticmethod
    def update_status(status_file, key, value):
        '''
        Update status and write to file
        '''
        status_data = Status.read_status(status_file)
        status_data[key] = value
        Status.create_status(status_data, status_file)

    @staticmethod
    def clear_status(status_file):
        '''
        Remove status
        '''
        if os.path.isfile(status_file):
            os.remove(status_file)

    @staticmethod
    def print_all_status():
        '''
        Read of status file and print instance name and status
        '''
        status_dir = verify_status_dir()
        if not os.listdir(status_dir):
            sys.exit('  You currently have no instance created')
        for item in os.listdir(status_dir):
            with open(os.path.join(status_dir, item)) as sfile:
                status = json.load(sfile)
            print '  {0}:  {1}'.format(status['Name'], status['State_Name'])
