#!/usr/bin/env python
import mock
import unittest
import sys


class StatusTest(unittest.TestCase):
    def setUp(self):
        global osMock, jsonMock, helperMock, verify_status_dirMock
        osMock = mock.MagicMock()
        jsonMock = mock.MagicMock()
        helperMock = mock.MagicMock()
        verify_status_dirMock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': osMock,
                                        'json': jsonMock,
                                        'helper': helperMock,
                                        'verify_status_dir': verify_status_dirMock})
        self.patcher.start()

        from ...status import Status

    def tearDown(self):
        self.patcher.stop()

    def test_create_status(self):
        pass

    def test_read_status(self):
        pass

    def test_update_status(self):
        pass

    def test_clear_status(self):
        pass

    def test_print_all_status(self):
        pass