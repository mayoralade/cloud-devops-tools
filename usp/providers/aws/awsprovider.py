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
from ... import helper
from ...status import Status
#Import service provider

TIMEOUT = 60
INTERVAL = 5


class AWSProvider(Provider):
    '''
        AWS Provider
    '''
    def __init__(self, config, logger):
        super(AWSProvider, self).__init__()
        self.instance = None
        self.config = AWSProvider.update_configuration(config)
        self.logger = logger
        #service holder
        self.interface = BotoInterface(self.config, self.logger)
        self.status_file = helper.construct_status_file_name(self.config.platform, self.config.name)
        self.update()

    def create(self):
        '''
        Instance creation interface
        '''
        self.logger.log.info('Creating Instance %s', self.config.name)
        #service_config = self.service_configuration()
        instance_id = self.interface.create_instance()#service_config)
        self.poll_for_state('running', instance_id)
        instance_data = self.interface.instance_data(instance_id)
        self.instance = Instance(instance_data, self.config.attribute_file, self.config.name)
        Status.create_status(self.instance.info, self.status_file)
        self.update_status_file('running')

    def start(self):
        '''
        Instance start up and login interface
        '''
        self.logger.log.info('Starting Instance %s', self.instance.Name)
        self.interface.start_instance(self.instance.InstanceId)
        self.update_status_file('running')

    def login(self):
        '''
        Instance start up and login interface
        '''
        self.logger.log.info('Logging into Instance %s', self.config.name)
        if self.config.platform == 'linux':
            os.system('ssh -i {0} ec2-user@{1}'.format(self.config.key_file_location,
                                                       self.instance.PublicIpAddress))
        else:
            self.logger.log.error('Only Linux has been implemented for AWS')

    def halt(self):
        '''
        Instance halt interface
        '''
        self.logger.log.info('Stopping Instance %s', self.instance.Name)
        self.interface.stop_instance(self.instance.InstanceId)
        self.update_status_file('stopped')

    def destroy(self):
        '''
        Instance deletion interface
        '''
        self.logger.log.info('Destroying Instance %s', self.config.name)
        self.interface.terminate_instance(self.instance.InstanceId)
        self.update_status_file('terminated')
        Status.clear_status(self.status_file)

    def status(self, instance_id=None, repeat=True):
        '''
        Instance Information interface
        '''
        if instance_id:
            status = self.interface.instance_status(instance_id)
        status = self.interface.instance_status(self.instance.InstanceId)
        if repeat:
            self.logger.log.info('%s is %s', self.config.name, status)
        return status

    @staticmethod
    def update_configuration(config):
        '''
        Update user defined config with default config for AWS
        '''
        provider_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            'machine.cfg')
        provider_config = helper.load_config_file(provider_config_path)
        for name, value in provider_config.items('default'):
            setattr(config, name, value)
        return config

    def service_configuration(self):
        '''
        Retrieve actual service configuration to pass at instance creation
        '''
        return self.config

    def update(self):
        '''
        Read instance data from tmp file created during instance creation
        '''
        if os.path.isfile(self.status_file):
            with open(self.status_file) as sfile:
                status_data = json.load(sfile)
            status_data = helper.flatten_dict(status_data)
            self.instance = Namespace()
            self.instance = helper.create_attribute_from_dict(Namespace(), status_data)

    def poll_for_state(self, state, instance_id=None):
        '''
            Wait for machine to get to desired state, timeout if it takes too long
        '''
        sleep_time = 0
        current_state = self.status(instance_id, repeat=False)
        self.logger.log.info('Instance is %s, please wait...', current_state)
        while current_state != state:
            current_state = self.status(instance_id, repeat=False)
            if sleep_time >= TIMEOUT:
                sys.exit('Instance is taking too long to reach %s state, exiting...', state)
            sleep(INTERVAL)
            sleep_time += INTERVAL
        self.logger.log.info('Instance is now %s', state)

    def update_status_file(self, state):
        '''
        Update Status of instance in status file
        '''
        self.poll_for_state(state)
        Status.update_status(self.status_file, 'State_Name', state)
