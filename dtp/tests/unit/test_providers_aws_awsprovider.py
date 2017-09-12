import mock
import unittest
import sys


class TestAWSProvider(unittest.TestCase):
    def setUp(self):
        global configMock, loggerMock, instanceMock, verifyMock
        instanceMock = mock.MagicMock()
        configMock = mock.MagicMock()
        loggerMock = mock.MagicMock()
        verifyMock = mock.MagicMock()
        self.patcher1 = mock.patch.dict('sys.modules',
                                        {'os': mock.MagicMock(),
                                         'json': mock.MagicMock(),
                                         'time': mock.MagicMock(),
                                         'argparse': mock.MagicMock(),
                                         'dtp.helper': mock.MagicMock(),
                                         'dtp.status': mock.MagicMock(),
                                         'dtp.providers.aws.interface': mock.MagicMock(),
                                         'dtp.providers.aws.instance': mock.MagicMock()})
        self.patcher1.start()

        self.patcher2 = mock.patch('dtp.providers.aws.awsprovider.helper',
            mock.MagicMock())

        from ...providers.aws import awsprovider
        self.aws = awsprovider
        self.patcher2.start()
        self.aws.os.path.isfile.return_value = False
        self.update_configuration = self.aws.AWSProvider.update_configuration
        self.aws.AWSProvider.update_configuration = mock.MagicMock()
        self.aws.AWSProvider.update_configuration.return_value = configMock
        configMock.platform = 'dev_test'
        self.aws.helper.construct_status_file_name.return_value = 'statusfile'
        self.update = self.aws.AWSProvider.update
        self.aws.AWSProvider.update = mock.MagicMock()
        self.awsprovider = self.aws.AWSProvider('test', 'config', loggerMock)
        self.verify = self.awsprovider.verify
        self.awsprovider.verify = verifyMock
        self.poll_for_state = self.awsprovider.poll_for_state
        self.update_status_file = self.awsprovider.update_status_file
        self.awsprovider.poll_for_state = mock.MagicMock()
        self.awsprovider.update_status_file = mock.MagicMock()
        self.awsprovider.instance = instanceMock

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_aws_provider_constructor(self):
        self.assertEqual(self.awsprovider.name, 'test')
        self.assertEqual(self.awsprovider.instance, instanceMock)
        self.assertEqual(self.awsprovider.config, configMock)
        self.assertEqual(self.awsprovider.logger, loggerMock)
        self.aws.AWSProvider.update_configuration.assert_called_once_with('config')
        self.aws.BotoInterface.assert_called_once_with('test', configMock, loggerMock)
        self.aws.helper.construct_status_file_name.assert_called_once_with('dev_test', 'test')
        self.awsprovider.update.assert_called_once()
        self.awsprovider.instance = instanceMock

    def test_create_already_existing_instance(self):
        self.awsprovider.instance = True
        with self.assertRaises(SystemExit) as _:
            self.awsprovider.create()
        self.awsprovider.logger.log.info.assert_called_once()

    def test_create_already_new_instance(self):
        configMock.attribute_file = 'myfile'
        self.awsprovider.instance = False
        self.awsprovider.interface.create_instance.return_value = 'mybox'
        self.awsprovider.interface.instance_data.return_value = 'mydata'
        self.aws.Instance.return_value = instanceMock
        instanceMock.info = 'myinfo'
        self.awsprovider.create()
        self.awsprovider.logger.log.info.assert_called_once()
        self.awsprovider.interface.create_instance.assert_called_once()
        self.awsprovider.poll_for_state.assert_called_once_with('running', 'mybox')
        self.awsprovider.interface.instance_data.assert_called_once_with('mybox')
        self.aws.Instance.assert_called_once_with('mydata', 'myfile', 'test')
        self.aws.Status.create_status.assert_called_once_with('myinfo', 'statusfile')

    def test_destroy(self):
        instanceMock.InstanceId = 123
        self.awsprovider.destroy()
        self.awsprovider.logger.log.info.assert_called_once()
        self.awsprovider.interface.terminate_instance.assert_called_once_with(123)
        self.awsprovider.update_status_file.assert_called_once_with('terminated')
        self.awsprovider.interface.delete_security_group.assert_called_once()
        self.aws.Status.clear_status('statusfile')

    def test_halt(self):
        instanceMock.InstanceId = 847
        self.awsprovider.halt()
        self.awsprovider.logger.log.info.assert_called_once()
        self.awsprovider.interface.stop_instance.assert_called_once_with(847)
        self.awsprovider.update_status_file.assert_called_once_with('stopped')

    def test_info(self):
        instance_dict = {'env': 'dev'}
        instanceMock.__dict__ = instance_dict
        self.awsprovider.info()
        output = sys.stdout.getvalue().strip('\n')
        self.assertEqual(output, '  env: dev')

    def test_login(self):
        instanceMock.PublicIpAddress = '10.0.0.0'
        self.awsprovider.login()
        self.awsprovider.logger.log.info.assert_called_once()
        self.awsprovider.interface.login_to_machine.assert_called_once_with('10.0.0.0')

    def test_start(self):
        instanceMock.InstanceId = 'myinstance'
        self.awsprovider.start()
        self.awsprovider.logger.log.info.assert_called_once()
        self.awsprovider.interface.start_instance.assert_called_once_with('myinstance')
        self.awsprovider.update_status_file.assert_called_once_with('running')

    def test_status_with_no_instanceid_with_repeat(self):
        instanceMock.InstanceId = 'no_id'
        self.awsprovider.interface.instance_status.return_value = 'eating'
        status = self.awsprovider.status()
        self.awsprovider.interface.instance_status.assert_called_once_with('no_id')
        self.awsprovider.logger.log.info.assert_called_once()
        self.assertEqual(status, 'eating')

    def test_status_with_instanceid_with_no_repeat(self):
        instanceMock.InstanceId = 'no_id'
        self.awsprovider.interface.instance_status.return_value = 'drinking'
        status = self.awsprovider.status(instance_id='my_id', repeat=False)
        self.awsprovider.interface.instance_status.assert_called_once_with('my_id')
        self.awsprovider.logger.log.info.assert_not_called()
        self.assertEqual(status, 'drinking')

    def test_pull(self):
        instanceMock.PublicIpAddress = 'x.x.x.x'
        self.awsprovider.pull()
        self.awsprovider.interface.sync_data.assert_called_once_with('pull', 'x.x.x.x')

    def test_push(self):
        instanceMock.PublicIpAddress = 'y.y.y.y'
        self.awsprovider.push()
        self.awsprovider.interface.sync_data.assert_called_once_with('push', 'y.y.y.y')

    def test_update_configuration(self):
        self.aws.os.path.join.return_value = '/tmp/junk'
        self.aws.helper.load_config_file.return_value = 'myprovider'
        self.aws.helper.configure_section_attributes.return_value = 'myattributes'
        new_config = self.update_configuration('myconfig')
        self.assertEqual(new_config, 'myattributes')
        self.aws.helper.load_config_file.assert_called_once_with('/tmp/junk')
        self.aws.helper.configure_section_attributes.assert_called_once_with(['default'], 'myprovider', 'myconfig')

    def test_update(self):
        self.aws.Namespace.return_value = 'mynamespace'
        self.aws.os.path.isfile.return_value = True
        self.aws.open = mock.MagicMock()
        self.aws.open.return_value.__enter__.return_value = 'myjsonfile'
        self.aws.json = mock.MagicMock()
        self.aws.json.load.return_value = 'myjsondata'
        self.aws.helper.flatten_dict.return_value = 'mystatusdata'
        self.aws.helper.create_attribute_from_dict.return_value = 'mynewattributes'
        self.update(self.awsprovider)
        self.aws.open.assert_called_once_with('statusfile')
        self.aws.json.load.assert_called_once_with('myjsonfile')
        self.aws.helper.flatten_dict.assert_called_once_with('myjsondata')
        self.aws.helper.create_attribute_from_dict.assert_called_once_with('mynamespace', 'mystatusdata')
        self.assertEqual(self.awsprovider.instance, 'mynewattributes')
        self.awsprovider.update = mock.MagicMock()

    def test_verify(self):
        self.awsprovider.instance = None
        with self.assertRaises(SystemExit) as _:
            self.verify()
        self.awsprovider.logger.log.error.assert_called_once()

    def test_poll_for_state_with_no_timeout(self):
        tmp_status = self.awsprovider.status
        self.awsprovider.status = mock.MagicMock()
        self.awsprovider.status.return_value = 'newstate'
        self.poll_for_state('newstate')
        self.assertEqual(self.awsprovider.logger.log.info.call_count, 2)
        self.awsprovider.status.assert_called_once_with(None, repeat=False)
        self.awsprovider.status = tmp_status

    def test_poll_for_state_with_timeout(self):
        tmp_status = self.awsprovider.status
        self.awsprovider.status = mock.MagicMock()
        self.awsprovider.status.return_value = 'oldstate'
        self.aws.TIMEOUT = 2
        self.aws.INTERVAL = 1
        with self.assertRaises(SystemExit) as _:
            self.poll_for_state('newstate')
        self.assertEqual(self.aws.sleep.call_count, 2)
        self.awsprovider.logger.log.info.assert_called_once()
        self.assertEqual(self.awsprovider.status.call_count, 4)
        self.awsprovider.status.assert_called_with(None, repeat=False)
        self.awsprovider.status = tmp_status

    def test_update_status_file(self):
        self.update_status_file('mystate')
        self.awsprovider.poll_for_state.assert_called_once_with('mystate')
        self.aws.Status.update_status.assert_called_once_with('statusfile', 'State_Name', 'mystate')
