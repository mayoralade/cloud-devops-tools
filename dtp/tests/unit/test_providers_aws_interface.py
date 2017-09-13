import mock
import unittest
import sys


class TestAWSInterface(unittest.TestCase):
    def setUp(self):
        global boto3Mock, configMock, keyFileMock, loggerMock, mapMock, CMMock
        boto3Mock = mock.MagicMock()
        configMock = mock.MagicMock()
        keyFileMock = mock.MagicMock()
        loggerMock = mock.MagicMock()
        mapMock = mock.MagicMock()
        CMMock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': mock.MagicMock(),
                                        'boto3': mock.MagicMock(),
                                        'botocore': mock.MagicMock(),
                                        'botocore.exceptions': mock.MagicMock(),
                                        'dtp.providers.aws.resources.ami_map': mock.MagicMock(),
                                        'dtp.devopstools.tools': mock.MagicMock()})

        self.patcher.start()

        #self.patcher2 = mock.patch('dtp.providers.aws.interface.botocore.exceptions',
        #                           mock.MagicMock())
        #self.patcher2.start()

        from ...providers.aws import interface
        self.interface = interface
        self.interface.boto3.client.return_value = boto3Mock
        configMock.access_key = 'access'
        configMock.secret_key = 'secret'
        self.boto = self.interface.BotoInterface(name='agege', config=configMock, logger=loggerMock)
        self.interface.botocore.exceptions.ClientError = Exception

    def tearDown(self):
        self.patcher.stop()
        #self.patcher2.stop()

    def test_aws_interface_constructor(self):
        self.assertEqual(self.boto.name, 'agege')
        self.assertEqual(self.boto.config, configMock)
        self.assertEqual(self.boto.logger, loggerMock)
        self.assertEqual(self.boto.client, boto3Mock)
        self.interface.boto3.client.assert_called_once_with('ec2',
                                                            aws_access_key_id='access',
                                                            aws_secret_access_key='secret')

    def test_verify_aws_key_for_new_key(self):
        configMock.key_name = 'named_key'
        configMock.key_file_location = 'key_location'
        key_dict = {'KeyMaterial': 'something'}
        self.boto.client.create_key_pair.return_value = key_dict
        self.interface.open = mock.MagicMock()
        self.interface.open.return_value.__enter__.return_value = keyFileMock
        self.boto.verify_aws_key()
        self.boto.client.create_key_pair.assert_called_once_with(KeyName='named_key')
        self.interface.open.assert_called_once_with('key_location', 'w')
        keyFileMock.write.assert_called_once_with('something')
        self.interface.os.chmod.assert_called_once_with('key_location', 0400)
        self.boto.logger.log.info.assert_called_once()

    def test_verify_aws_key_for_existing_key(self):
        self.boto.client.create_key_pair.side_effect = self.interface.botocore.exceptions.ClientError
        self.boto.verify_aws_key()
        self.boto.logger.log.warning.assert_called_once()

    def test_create_instance_with_no_existing_sg(self):
        tmp_get_ami_image = self.boto.get_ami_image
        tmp_verify_aws_key = self.boto.verify_aws_key
        tmp_get_service_config = self.boto.get_service_config
        tmp_create_security_group = self.boto.create_security_group
        tmp_configure_security_group = self.boto.configure_security_group
        self.boto.get_ami_image = mock.MagicMock()
        self.boto.verify_aws_key = mock.MagicMock()
        self.boto.get_service_config = mock.MagicMock()
        self.boto.create_security_group = mock.MagicMock()
        self.boto.configure_security_group = mock.MagicMock()
        self.boto.create_security_group.return_value = False
        instance_dict = {'Instances': [{'InstanceId': 'instance1'}]}
        self.boto.client.run_instances.return_value = instance_dict
        my_instance = self.boto.create_instance()
        self.assertEqual(self.boto.logger.log.info.call_count, 2)
        self.boto.get_ami_image.assert_called_once()
        self.boto.verify_aws_key.assert_called_once()
        self.boto.get_service_config.assert_called_once()
        self.boto.create_security_group.assert_called_once_with('agege_sg_group')
        self.boto.client.run_instances.assert_called_once()
        self.boto.configure_security_group.assert_called_once_with('agege_sg_group')
        self.assertEqual(my_instance, 'instance1')
        self.boto.get_ami_image = tmp_get_ami_image
        self.boto.verify_aws_key = tmp_verify_aws_key
        self.boto.get_service_config = tmp_get_service_config
        self.boto.create_security_group = tmp_create_security_group
        self.boto.configure_security_group = tmp_configure_security_group

    def test_create_instance_with_existing_sg(self):
        tmp_get_ami_image = self.boto.get_ami_image
        tmp_verify_aws_key = self.boto.verify_aws_key
        tmp_get_service_config = self.boto.get_service_config
        tmp_create_security_group = self.boto.create_security_group
        tmp_configure_security_group = self.boto.configure_security_group
        self.boto.get_ami_image = mock.MagicMock()
        self.boto.verify_aws_key = mock.MagicMock()
        self.boto.get_service_config = mock.MagicMock()
        self.boto.create_security_group = mock.MagicMock()
        self.boto.configure_security_group = mock.MagicMock()
        self.boto.create_security_group.return_value = True
        self.boto.create_instance()
        self.boto.configure_security_group.assert_not_called()
        self.boto.get_ami_image = tmp_get_ami_image
        self.boto.verify_aws_key = tmp_verify_aws_key
        self.boto.get_service_config = tmp_get_service_config
        self.boto.create_security_group = tmp_create_security_group
        self.boto.configure_security_group = tmp_configure_security_group

    def test_create_security_group_when_sg_does_not_exists(self):
        self.assertFalse(self.boto.create_security_group('yegbe'))
        self.boto.client.create_security_group.assert_called_once()

    def test_create_security_group_when_sg_exists(self):
        self.boto.client.create_security_group.side_effect = self.interface.botocore.exceptions.ClientError
        self.assertTrue(self.boto.create_security_group('yegbe'))
        self.boto.client.create_security_group.assert_called_once()
        self.boto.logger.log.warning.assert_called_once()

    def test_configure_security_group_without_exceptions(self):
        configMock.ports = [44]
        self.boto.configure_security_group('gbengbeleku')
        self.boto.client.authorize_security_group_ingress.assert_called_once_with(GroupName='gbengbeleku',
                                                                                  IpProtocol="tcp",
                                                                                  CidrIp="0.0.0.0/0",
                                                                                  FromPort=int(44),
                                                                                  ToPort=int(44))

    def test_configure_security_group_with_exceptions(self):
        configMock.ports = [44]
        self.boto.client.authorize_security_group_ingress.side_effect = self.interface.botocore.exceptions.ClientError
        self.boto.configure_security_group('gbengbeleku')
        self.boto.client.authorize_security_group_ingress.assert_called_once_with(GroupName='gbengbeleku',
                                                                                  IpProtocol="tcp",
                                                                                  CidrIp="0.0.0.0/0",
                                                                                  FromPort=int(44),
                                                                                  ToPort=int(44))
        self.boto.logger.log.warning.assert_called_once()

    def test_delete_security_group(self):
        self.boto.delete_security_group('yoyo')
        self.boto.client.delete_security_group.assert_called_once_with(GroupId='yoyo')

    def test_start_instance(self):
        self.boto.start_instance('boyo')
        self.boto.client.start_instances.assert_called_once_with(InstanceIds=['boyo'])

    def test_stop_instance(self):
        self.boto.stop_instance('fowo')
        self.boto.client.stop_instances.assert_called_once_with(InstanceIds=['fowo'])

    def test_terminate_instances(self):
        self.boto.terminate_instance('play')
        self.boto.client.terminate_instances.assert_called_once_with(InstanceIds=['play'])

    def test_instance_data(self):
        instance_dict = {'Reservations': [{'Instances': ['instance_data']}]}
        self.boto.client.describe_instances.return_value = instance_dict
        mydata = self.boto.instance_data('gbogbo')
        self.boto.client.describe_instances.assert_called_once_with(InstanceIds=['gbogbo'])
        self.assertEqual(mydata, 'instance_data')

    def test_instance_status(self):
        tmp_instance_data = self.boto.instance_data
        self.boto.instance_data = mock.MagicMock()
        state_dict = {'State': {'Name': 'me'}}
        self.boto.instance_data.return_value = state_dict
        mystatus = self.boto.instance_status('gafo')
        self.boto.instance_data.assert_called_once_with('gafo')
        self.assertEqual(mystatus, 'me')
        self.boto.instance_data = tmp_instance_data

    def test_get_ami_image(self):
        configMock.platform = 'ojota'
        configMock.os_name = 'eko'
        self.interface.os.path.join.return_value = 'yanafile'
        self.interface.AMIMap.return_value = mapMock
        mapMock.get_ami_image.return_value = 'agegebread'
        myimage = self.boto.get_ami_image()
        self.interface.AMIMap.assert_called_once_with('ojota', 'eko', 'yanafile')
        self.assertEqual(myimage, 'agegebread')

    def test_login_to_machine_for_linux(self):
        configMock.platform = 'linux'
        configMock.key_file_location = 'new_location'
        self.boto.login_to_machine('x.x.x.x')
        self.interface.os.system.assert_called_once_with('ssh -o "StrictHostKeyChecking no" -i new_location ec2-user@x.x.x.x')
        self.boto.logger.log.error.assert_not_called()

    def test_login_to_machine_for_non_linux(self):
        configMock.platform = 'yaba'
        self.boto.login_to_machine('x.x.x.x')
        self.boto.logger.log.error.assert_called_once()

    def test_sync_data_for_linux(self):
        configMock.platform = 'linux'
        configMock.local_sync_directory = ['mydir']
        tmp_construct_rsync_command = self.boto.construct_rsync_command
        self.boto.construct_rsync_command = mock.MagicMock()
        self.boto.construct_rsync_command.return_value = 'tryam'
        self.boto.sync_data('jembe', 'y.y.y.y')
        self.boto.construct_rsync_command.assert_called_once_with('jembe', 'mydir', 'y.y.y.y')
        self.interface.os.system.assert_called_once_with('tryam')
        self.assertEqual(self.boto.logger.log.info.call_count, 2)
        self.boto.logger.log.error.assert_not_called()
        self.boto.construct_rsync_command = tmp_construct_rsync_command

    def test_sync_data_for_non_linux(self):
        configMock.platform = 'panda'
        configMock.local_sync_directory = ['mydir']
        self.boto.sync_data('jembe', 'y.y.y.y')
        self.interface.os.system.assert_not_called()
        self.assertEqual(self.boto.logger.log.info.call_count, 2)
        self.boto.logger.log.error.assert_called_once()

    def test_construct_pull_rsync_command(self):
        configMock.key_file_location = 'isolo'
        self.interface.os.path.basename.return_value = 'lekki'
        mypull = self.boto.construct_rsync_command('pull', 'nibi', 'bariga')
        self.assertEqual(mypull, 'rsync -ae "ssh -i isolo" ec2-user@bariga:/home/ec2-user/lekki/ nibi')
        self.interface.os.path.basename.assert_called_once_with('nibi')

    def test_construct_push_rsync_command(self):
        configMock.key_file_location = 'ojota'
        self.interface.os.path.basename.return_value = 'ajah'
        mypush = self.boto.construct_rsync_command('push', 'yaba', 'sango')
        self.assertEqual(mypush, 'rsync -ae "ssh -i ojota" yaba ec2-user@sango:/home/ec2-user')

    def test_get_service_config(self):
        configMock.services = 'loba'
        self.interface.DevOpsTools.return_value = CMMock
        CMMock.aggregate_configs.return_value = 'pompeii'
        myservice = self.boto.get_service_config()
        self.assertEqual(myservice, 'pompeii')
        self.interface.DevOpsTools.assert_called_once_with('loba', loggerMock)
