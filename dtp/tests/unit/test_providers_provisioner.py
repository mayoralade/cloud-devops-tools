#!/usr/bin/env python
import mock
import unittest
import sys


class ProvisionerTest(unittest.TestCase):
    def setUp(self):
        global osMock, jsonMock, importlibMock, loggingMock
        osMock = mock.MagicMock()
        jsonMock = mock.MagicMock()
        loggingMock = mock.MagicMock()
        importlibMock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': osMock,
                                        'json': jsonMock,
                                        'importlib': importlibMock,
                                        'logging': loggingMock})
        self.patcher.start()

        from ...providers.provisioner import Provisioner

    def tearDown(self):
        self.patcher.stop()

    def test_verify_provider(self):
        pass

    def test_run_command_by_provider(self):
        pass

    def test_update_providers(self):
        pass
