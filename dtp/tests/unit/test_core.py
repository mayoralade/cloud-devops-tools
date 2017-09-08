#!/usr/bin/env python
import mock
import unittest
import sys


class CoreTest(unittest.TestCase):
    def setUp(self):
        global osPathMock, copy2Mock
        osPathMock = mock.MagicMock()
        copy2Mock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': mock.MagicMock(),
                                        'shutil': mock.MagicMock(),
                                        'argparse': mock.MagicMock()})
        self.patcher.start()

        global core
        from ... import core
        self.patcher2 = mock.patch('dtp.core.Status', mock.MagicMock())
        self.patcher3 = mock.patch('dtp.core.DevOpsTools', mock.MagicMock())
        self.core = core
        self.core.os.path = osPathMock
        self.core.copy2 = copy2Mock
        self.mock = mock.MagicMock()
        self.patcher2.start()
        self.patcher3.start()

    def tearDown(self):
        self.patcher.stop()
        self.patcher2.stop()
        self.patcher3.stop()

    def test_construct_config_path(self):
        osPathMock.join.return_value = '/tmp/dude'
        config_path = self.core.construct_config_path('/tmp', 'junk')
        self.assertEqual(config_path, '/tmp/dude.cfg')

    def test_copy_config_template_user_template_exists(self):
        osPathMock.isfile.return_value = True
        with self.assertRaises(SystemExit) as _:
            self.core.copy_config_template('/tmp/junk')

    def test_copy_config_template_user_template_not_exists(self):
        osPathMock.join.return_value = '/tmp/junk_src'
        osPathMock.isfile.return_value = False
        copy2Mock.return_value = None
        self.core.copy_config_template('/tmp/junk')
        copy2Mock.assert_called_once_with('/tmp/junk_src', '/tmp/junk')

    def test_load_config_files_config_exists(self):
        self.core.construct_config_path = mock.MagicMock(return_value=True)
        self.core.copy_config_template = mock.MagicMock(return_value=True)
        osPathMock.isfile.return_value = True
        self.assertTrue(self.core.load_config_files('given', 'default'))

    def test_load_config_files_no_config_exists(self):
        self.core.construct_config_path = mock.MagicMock()
        self.core.copy_config_template = mock.MagicMock()
        osPathMock.isfile.return_value = False
        with self.assertRaises(SystemExit) as _:
            self.core.load_config_files('given', 'default')

    def test_define_config_attributes(self):
        self.tmp_config = self.core.load_config_files
        self.tmp_helper = self.core.helper.configure_section_attributes
        self.core.load_config_files = mock.MagicMock()
        self.core.Namespace = mock.MagicMock(return_value='works')
        self.core.helper.load_config_file = mock.MagicMock(return_value=self.mock)
        self.core.helper.configure_section_attributes = mock.MagicMock(return_value=None)
        self.core.helper.load_config_file.return_value.get.return_value = True
        self.core.define_config_attributes('dummy')
        self.core.helper.configure_section_attributes.assert_called_once_with(
            ['resource', True, 'services'], self.mock, 'works')
        self.core.load_config_files = self.tmp_config
        self.core.helper.configure_section_attributes = self.tmp_helper

    def test_manage_resource(self):
        self.core.Provisioner = mock.MagicMock()
        self.core.manage_resource('a', 'b', 'c', 'd')
        self.core.Provisioner.return_value.run_command_by_provider.assert_called_once_with()

    def test_run_command_list_tools(self):
        args = mock.MagicMock(action='list')
        prop = mock.PropertyMock(return_value='tools')
        type(args).name = prop
        self.core.run_command(args)
        self.core.DevOpsTools.list_tools.assert_called_once_with()

    def test_run_command_list_vms(self):
        args = mock.MagicMock(action='list')
        prop = mock.PropertyMock(return_value='vms')
        type(args).name = prop
        self.core.run_command(args)
        self.core.Status.print_all_status.assert_called_once_with()
