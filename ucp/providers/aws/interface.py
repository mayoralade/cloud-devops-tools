'''
    AWS Boto3 interface abstraction for loose coupling
'''
import os
import boto3
import botocore.exceptions
from .resources.ami_map import AMIMap


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
        group_id = self.create_security_group()
        instance = self.client.run_instances(ImageId=ami_image,
                                             MinCount=int(self.config.min_count),
                                             MaxCount=int(self.config.max_count),
                                             KeyName=self.config.key_name,
                                             InstanceType=self.config.machine_type,
                                             SecurityGroupIds=[group_id],
                                             Placement={'AvailabilityZone': self.config.az},
                                             Monitoring={'Enabled': False})#,
                                             #UserData=service_config)
        self.configure_security_group(group_id)
        return instance['Instances'][0]['InstanceId']

    def create_security_group(self):
        '''
        Create New security group for instance
        '''
        response = self.client.create_security_group(
            Description='Default security group for {0}'.format(self.name),
            GroupName='{0}_sg_group'.format(self.name)
        )
        return response['GroupId']

    def configure_security_group(self, group_id):
        '''
        Configure security group for defined ports
        '''
        for port in self.config.ports:
            self.client.authorize_security_group_ingress(GroupId=group_id,
                                                         IpProtocol="tcp",
                                                         CidrIp="0.0.0.0/0",
                                                         FromPort=port,
                                                         ToPort=port)

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

    #def clean_up(self, instance):
        # delete security group
        # delete

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
