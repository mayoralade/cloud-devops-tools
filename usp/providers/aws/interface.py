'''
    AWS Boto3 interface abstraction for loose coupling
'''
import os
import boto3
import botocore.exceptions
from ..resources.ami_map import AMIMap
from ....logging.logger import Logger


class BotoInterface(object):
    '''
        Boto3 Interface to decouple AWSProvider from Python SDK
    '''
    def __init__(self, config):
        self.config = config
        self.client = None
        self.create_client()
        self.log = Logger()

    def create_client(self):
        '''
        Create an EC2 client with the user credentials
        '''
        self.client = boto3.client('ec2',
                                   aws_access_key_id=self.config.access_key,
                                   aws_secret_access_key=self.config.secret_key)

    def verify_aws_key(self):
        '''
        Try to create AWS Key, if it already exist, log it
        '''
        try:
            key_pair = self.client.create_key_pair(KeyName=self.config.key_name)
            with open(self.config.key_file_location, 'w') as kpfile:
                kpfile.write(key_pair['KeyMaterial'])
                os.chmod(self.config.key_file_location, 0400)
            self.log.info('Key: %s successfully created', self.config.key_name)
        except botocore.exceptions.ClientError:
            self.log.info('Key: %s already exists, moving on', self.config.key_name)

    def create_instance(self):#, service_config):
        '''
        Create an EC2 instance
        '''
        self.log.info('Creating EC2 instance, please wait...')
        ami_image = self.get_ami_image()
        self.verify_aws_key()
        instance = self.client.run_instances(ImageId=ami_image,
                                             MinCount=self.config.min_count,
                                             MaxCount=self.config.max_count,
                                             KeyName=self.config.key_name,
                                             InstanceType=self.config.machine_type,
                                             Placement={'AvailabilityZone': self.config.az},
                                             Monitoring={'Enabled': False})#,
                                             #UserData=service_config)
        self.configure_security_group()
        return instance['Instances'][0]['InstanceId']

    def configure_security_group(self):
        '''
        Configure instance security group
        '''
        # Future update, enable fine turning to port and protocol level
        self.client.authorize_security_group_ingress(
            FromPort=-1,
            IpProtocol=-1,
            ToPort=-1)

    def start_instance(self, instance_id):
        '''
        Start Instance
        '''
        self.client.start_instances(InstanceIds=[instance_id])

    def stop_instance(self, instance_id):
        '''
        Stop Instance
        '''
        self.client.stop_instances(InstanceIds=[instance_id])

    def terminate_instance(self, instance_id):
        '''
        Stop Instance
        '''
        self.client.terminate_instances(InstanceIds=[instance_id])

    def instance_status(self, instance_id):
        '''
        Get the statue of an instance
        '''
        instance_state = self.client.describe_instances(InstanceIds=[instance_id])
        return instance_state['InstanceStatuses'][0]['InstanceState']['Name']

    def get_ami_image(self):
        '''
        Get AMI ID
        '''
        ami_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                self.config.ami_file)
        ami_map = AMIMap(self.config.platform, self.config.os_name, ami_file)
        return ami_map.get_ami_image()
