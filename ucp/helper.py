'''
Library of Helper functions
'''
import sys
import os
import re
import ConfigParser
from flatten_dict import flatten


def underscore_reducer(key1, key2):
    '''
    Underscore reducer for flatten dictionary
    '''
    if key1 is None:
        return key2
    return key1 + "_" + key2

def verify_status_dir():
    '''
    Verify status dir exists, else create it
    '''
    if sys.platform == 'win32':
        root_path = r'C:\Users\Public\ucp\\'
    else:
        root_path = '/tmp/ucp/'
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    return root_path

def construct_status_file_name(provider, instance_name):
    '''
    Construct hidden tmp file to hold instance status
    '''
    root_path = verify_status_dir()
    return r'{0}.{1}_{2}.tmp'.format(root_path, provider, instance_name)

def create_attribute_from_dict(class_name, class_dict):
    '''
    Dynamically add attributes from dictionary to class
    '''
    for key, value in class_dict.iteritems():
        setattr(class_name, key, value)
    return class_name

def flatten_dict(given_dict):
    '''
    flatten dict
    '''
    return flatten(given_dict, reducer=underscore_reducer)

def load_config_file(config_file_path):
    '''
    Load program config file
    '''
    config = ConfigParser.RawConfigParser()
    config.read(config_file_path)
    return config

def configure_section_attributes(sections, config_data, config):
    '''
    Read config file, generate configuration attributes from
    sections passed to function
    '''
    for section in sections:
        for name, value in config_data.items(section):
            check_for_list = re.match(r'\[(.*)\]', value)
            if check_for_list:
                value = check_for_list.group(1).split(',')
                if not value:
                    continue
            setattr(config, name, value)
    return config
