'''
Manage instance status
'''
import json
import os


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
