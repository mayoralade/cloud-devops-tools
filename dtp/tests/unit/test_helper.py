#!/usr/bin/env python
import mock
import unittest
import sys


class HelperTest(unittest.TestCase):
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

        from ... import helper

    def tearDown(self):
        self.patcher.stop()

    def test_underscore_reducer(self):
        pass

    def test_verify_status_dir(self):
        pass

    def test_construct_status_file_name(self):
        pass

    def test_create_attribute_from_dict(self):
        pass

    def test_flatten_dict(self):
        pass

    def test_load_config_file(self):
        pass

    def test_configure_section_attributes(self):
        pass
