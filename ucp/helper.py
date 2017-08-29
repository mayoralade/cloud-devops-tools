'''
Library of Helper functions
'''
import sys
import ConfigParser
from flatten_dict import flatten


def underscore_reducer(key1, key2):
    '''
    Underscore reducer for flatten dictionary
    '''
    if key1 is None:
        return key2
    return key1 + "_" + key2

def construct_status_file_name(provider, instance_name):
    '''
    Construct hidden tmp file to hold instance status
    '''
    if sys.platform == 'win32':
        return r'C:\Users\Public\.{0}_{1}.tmp'.format(provider, instance_name)
    return '/tmp/.{0}_{1}.tmp'.format(provider, instance_name)

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
            if ',' in value:
                value = [int(i) for i in value.split(',')]
            setattr(config, name, value)
    return config
