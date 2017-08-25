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
        self.status = None

    @abstractmethod
    def create_instance(self):
        '''
        Instance creation interface
        '''
        pass

    @abstractmethod
    def start_instance(self):
        '''
        Instance start up and login interface
        '''
        pass

    @abstractmethod
    def enter_instance(self):
        '''
        Instance start up and login interface
        '''
        pass

    @abstractmethod
    def halt_instance(self):
        '''
        Instance halt interface
        '''
        pass

    @abstractmethod
    def destroy_instance(self):
        '''
        Instance deletion interface
        '''
        pass

    @abstractmethod
    def instance_status(self):
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
