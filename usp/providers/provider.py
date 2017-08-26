'''
    Abstract Provider class
'''
from abc import ABCMeta, abstractmethod


class Provider(object):
    '''
        Provider abstract base class for interface verification
    '''
    __metaclass__ = ABCMeta
    def __init__(self):
        self.config = None

    @abstractmethod
    def create(self):
        '''
        Instance creation interface
        '''
        pass

    @abstractmethod
    def start(self):
        '''
        Instance start up and login interface
        '''
        pass

    @abstractmethod
    def login(self):
        '''
        Instance login interface
        '''
        pass

    @abstractmethod
    def halt(self):
        '''
        Instance halt interface
        '''
        pass

    @abstractmethod
    def destroy(self):
        '''
        Instance deletion interface
        '''
        pass

    @abstractmethod
    def status(self):
        '''
        Instance Information interface
        '''
        pass

    @abstractmethod
    def service_configuration(self):
        '''
        Service Configuration Interface
        '''
        pass
