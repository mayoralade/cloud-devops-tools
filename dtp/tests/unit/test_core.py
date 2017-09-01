#!/usr/bin/env python
import mock
import unittest
import sys


class CoreTest(unittest.TestCase):
    def setUp(self):
        global osMock, shutilMock, argparseMock, helperMock, providersMock, devopstoolsMock, statusMock
        osMock = mock.MagicMock()
        shutilMock = mock.MagicMock()
        argparseMock = mock.MagicMock()
        helperMock = mock.MagicMock()
        providersMock = mock.MagicMock()
        devopstoolsMock = mock.MagicMock()
        statusMock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': osMock,
                                        'shutil': shutilMock,
                                        'argparse': argparseMock,
                                        'helper': helperMock,
                                        'provider': providersMock,
                                        'devopstools': devopstoolsMock,
                                        'status': statusMock})
        self.patcher.start()

        from ... import core

    def tearDown(self):
        self.patcher.stop()

    def test_construct_config_path(self):
        pass

    def test_copy_config_template(self):
        pass

    def test_load_config_files(self):
        pass

    def test_define_config_attributes(self):
        pass

    def test_manage_resource(self):
        pass

    def test_run_command(self):
        pass
