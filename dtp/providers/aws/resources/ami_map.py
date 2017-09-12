'''
This maps a platform and os name to a give AMI
# Improvement will be to dynamically find the image
# from a set of attributes rather than hardcoding
# the AMI IDs
'''
import json


class AMIMap(object):
    '''
    Manage mappings between a platform and os to AMI ID
    '''
    def __init__(self, platform, os_name, ami_file):
        self.platform = platform
        self.os_name = os_name
        self.ami_file = ami_file
        self.ami_map = None

    def ami_mappings(self):
        '''
        Define Mappings
        '''
        with open(self.ami_file) as ami_data:
            mappings = json.load(ami_data)
        return mappings

    def get_ami_image(self):
        '''
        Return AMI Image if in map
        '''
        self.ami_map = self.ami_mappings()
        return self.ami_map.get(self.platform).get(self.os_name)
