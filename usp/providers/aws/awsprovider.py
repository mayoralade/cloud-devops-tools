'''
Main AWS Provider class
'''
import os
import sys
import json
from time import sleep
from argparse import Namespace
from ..provider import Provider
from .interface import BotoInterface
from .instance import Instance
from .resources import helper
from ....logging.logger import Logger
from ....status import Status
#Import service provider

TIMEOUT = 60
INTERVAL = 2


class AWSProvider(Provider):
    '''
        AWS Provider
    '''
    def __init__(self, config):
        super(AWSProvider, self).__init__()
        self.instance = None
        self.config = self.update_configuration(config)
        self.log = Logger()
        #service holder
        #get default machine config and merge with given config
        self.interface = BotoInterface(self.config)
        self.status_file = helper.construct_status_file_name(self.config.platform, self.config.name)
        self.try_update_instance()

    def create_instance(self):
        '''
        Instance creation interface
        '''
        self.log.info('Creating Instance Instance %s', self.config.name)
        service_config = self.service_configuration()
        instance_data = self.interface.create_instance(service_config)
        self.instance = Instance(instance_data, self.config.attribute_file, self.config.name)
        Status.create_status(self.instance.data, self.status_file)
        self.update_status_file('running')

    def start_instance(self):
        '''
        Instance start up and login interface
        '''
        self.log.info('Starting Instance %s', self.instance.Name)
        self.interface.start_instance(self.instance.InstanceId)
        self.update_status_file('running')

    def enter_instance(self):
        '''
        Instance start up and login interface
        '''
        self.log.info('Logging into Instance %s', self.instance.Name)
        if self.config.platform == 'linux':
            os.system('ssh -i {0} ec2-user@{1}'.format(self.config.key_file_location,
                                                       self.instance.PublicIpAddress))
        else:
            self.log.error('Only Linux has been implemented for AWS')

    def halt_instance(self):
        '''
        Instance halt interface
        '''
        self.log.info('Stopping Instance %s', self.instance.Name)
        self.interface.stop_instance(self.instance.InstanceId)
        self.update_status_file('stopped')

    def destroy_instance(self):
        '''
        Instance deletion interface
        '''
        self.log.info('Destroying Instance %s', self.instance.Name)
        self.interface.terminate_instance(self.instance.InstanceId)
        self.update_status_file('terminated')

    def instance_status(self):
        '''
        Instance Information interface
        '''
        return self.interface.instance_status(self.instance.InstanceId)

    def update_configuration(self, config):
        '''
        Update user defined config with default config for AWS
        '''
        self.config = config
        return self.config

    def service_configuration(self):
        '''
        Retrieve actual service configuration to pass at instance creation
        '''
        return self.config

    def try_update_instance(self):
        '''
        Read instance data from tmp file created during instance creation
        '''
        if os.path.isfile(self.status_file):
            with open(self.status_file) as sfile:
                status_data = json.load(sfile)
            status_data = helper.flatten_dict(status_data)
            self.instance = Namespace()
            self.instance = helper.create_attribute_from_dict(Namespace(), status_data)

    def poll_for_state(self, state):
        '''
            Wait for machine to get to desired state, timeout if it takes too long
        '''
        sleep_time = 0
        current_state = self.instance_status()
        while current_state != state:
            current_state = self.instance_status()
            self.log.info('Instance is %s', current_state)
            if sleep_time >= TIMEOUT:
                sys.exit('Instance is taking too long to reach %s state, exiting...', state)
            sleep(INTERVAL)
            sleep_time += INTERVAL

    def update_status_file(self, state):
        '''
        Update Status of instance in status file
        '''
        self.poll_for_state(state)
        Status.update_status(self.status_file, 'State_Name', state)
