'''
    AWS Boto3 interface abstraction for loose coupling
'''
import os
import boto3
import botocore.exceptions
from .resources.ami_map import AMIMap
from ...devoptools.tools import DevOpsTools


class BotoInterface(object):
    '''
        Boto3 Interface to decouple AWSProvider from Python SDK
    '''
    def __init__(self, name, config, logger):
        self.name = name
        self.config = config
        self.client = None
        self.create_client()
        self.logger = logger

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
            self.logger.log.info('Key: %s successfully created', self.config.key_name)
        except botocore.exceptions.ClientError:
            self.logger.log.warning('Key: %s already exists, moving on', self.config.key_name)

    def create_instance(self):#, service_config):
        '''
        Create an EC2 instance
        '''
        self.logger.log.info('Creating EC2 instance, please wait...')
        ami_image = self.get_ami_image()
        self.verify_aws_key()
        config_manager = self.get_service_config()
        sec_group_name = '{0}_sg_group'.format(self.name)
        sg_exists = self.create_security_group(sec_group_name)
        instance = self.client.run_instances(ImageId=ami_image,
                                             MinCount=int(self.config.min_count),
                                             MaxCount=int(self.config.max_count),
                                             KeyName=self.config.key_name,
                                             InstanceType=self.config.machine_type,
                                             SecurityGroups=[sec_group_name],
                                             Placement={'AvailabilityZone': self.config.az},
                                             Monitoring={'Enabled': False},
                                             UserData=config_manager)
        if not sg_exists:
            self.configure_security_group(sec_group_name)
        return instance['Instances'][0]['InstanceId']

    def create_security_group(self, sec_group_name):
        '''
        Create New security group for instance
        '''
        sg_exists = False
        try:
            _ = self.client.create_security_group(
                Description='Default security group for {0}'.format(self.name),
                GroupName=sec_group_name
            )
        except botocore.exceptions.ClientError:
            sg_exists = True
            self.logger.log.warning('Creation failed, {0} already exists...'.format(sec_group_name))
        return sg_exists

    def configure_security_group(self, group_name):
        '''
        Configure security group for defined ports
        '''
        for port in self.config.ports:
            self.client.authorize_security_group_ingress(GroupName=group_name,
                                                         IpProtocol="tcp",
                                                         CidrIp="0.0.0.0/0",
                                                         FromPort=int(port),
                                                         ToPort=int(port))

    def delete_security_group(self, group_id):
        '''
        Delete Security Group Id
        '''
        self.client.delete_security_group(GroupId=group_id)

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

    def instance_data(self, instance_id):
        '''
        Get the statue of an instance
        '''
        instance_state = self.client.describe_instances(InstanceIds=[instance_id])
        return instance_state['Reservations'][0]['Instances'][0]

    def instance_status(self, instance_id):
        '''
        Get the statue of an instance
        '''
        instance_state = self.instance_data(instance_id)
        return instance_state['State']['Name']

    def get_ami_image(self):
        '''
        Get AMI ID
        '''
        ami_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                self.config.ami_file)
        ami_map = AMIMap(self.config.platform, self.config.os_name, ami_file)
        return ami_map.get_ami_image()

    def login_to_machine(self, ip_address):
        '''
        Enable ssh or rdp to instance
        '''
        if self.config.platform == 'linux':
            os.system('ssh -o "StrictHostKeyChecking no" -i {0} ec2-user@{1}'.format(
                self.config.key_file_location,
                ip_address))
        else:
            self.logger.log.error('Only Linux has been implemented for AWS')

    def get_service_config(self):
        '''
        Get the services to be configured on machine
        and pass as userdata for amazon instance creation
        '''
        config_manager = DevOpsTools(self.config.services)
        return config_manager.aggregate_config
