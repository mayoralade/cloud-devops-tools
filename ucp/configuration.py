'''
    Abstract Configuration class
'''
from abc import ABCMeta, abstractmethod


class Configuration(object):
    '''
        Configuration abstract base class for interface verification
    '''
    __metaclass__ = ABCMeta
    def __init__(self):
        self.config = None

    @abstractmethod
    def read_config(self):
        '''
        Read Configuration interface
        '''
        pass
