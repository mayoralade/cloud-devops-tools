#!/usr/bin/env python
import mock
import unittest
import sys
from mock import MagicMock


class HelperTest(unittest.TestCase):
    def setUp(self):
        global osPathMock, osMakeDirsMock, sysMock, reMock
        osPathMock = MagicMock()
        osMakeDirsMock = MagicMock()
        sysMock = MagicMock()
        reMock = MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': MagicMock(),
                                        're': MagicMock(),
                                        'ConfigParser': MagicMock(),
                                        'flatten_dict': MagicMock()})
        self.patcher.start()

        from ... import helper
        self.helper = helper
        self.helper.os.path = osPathMock
        self.helper.os.makedirs = osMakeDirsMock
        self.helper.sys = sysMock
        self.helper.re = reMock

    def tearDown(self):
        self.patcher.stop()

    def test_underscore_reducer_with_two_keys(self):
        uredux = self.helper.underscore_reducer('a', 'b')
        self.assertEqual(uredux, 'a_b')

    def test_underscore_reducer_with_no_first_key(self):
        uredux = self.helper.underscore_reducer(None, 'b')
        self.assertEqual(uredux, 'b')

    def test_underscore_reducer_with_no_second_key(self):
        with self.assertRaises(TypeError) as _:
            self.helper.underscore_reducer('a', None)

    def test_verify_status_dir_none_windows_and_path_does_not_exists(self):
        self.helper.sys = mock.MagicMock(platform='linux')
        osPathMock.exists.return_value = False
        dir_path = self.helper.verify_status_dir()
        self.assertEqual(dir_path, '/tmp/dtp/')

    def test_verify_status_dir_win32_path_exists(self):
        self.helper.sys = mock.MagicMock(platform='win32')
        osPathMock.exists.return_value = True
        dir_path = self.helper.verify_status_dir()
        self.assertEqual(dir_path, r'C:\Users\Public\dtp\\')

    def test_verify_status_dir_win32_path_does_not_exists(self):
        self.helper.sys = mock.MagicMock(platform='win32')
        osPathMock.exists.return_value = False
        dir_path = self.helper.verify_status_dir()
        osMakeDirsMock.assert_called_once_with(dir_path)
        self.assertEqual(dir_path, r'C:\Users\Public\dtp\\')

    def test_construct_status_file_name(self):
        verify_container = self.helper.verify_status_dir
        self.helper.verify_status_dir = mock.MagicMock(return_value='/tmp/junk/')
        status_fn = self.helper.construct_status_file_name('dtp', 'inst_1')
        self.assertEqual(status_fn, r'/tmp/junk/.dtp_inst_1.tmp')
        self.helper.verify_status_dir = verify_container

    def test_create_attribute_from_dict(self):
        test_dict = {'a': 1, 'b': 2}
        my_class = MagicMock()
        obj_dict = self.helper.create_attribute_from_dict(my_class, test_dict)
        self.assertEqual(obj_dict.a, 1)
        self.assertEqual(obj_dict.b, 2)

    def test_configure_section_attributes(self):
        sections = ['one']
        config_data = MagicMock()
        test_dict = {'a': '[2, 3]'}
        config_data.items.return_value = test_dict.items()
        reMock.match.return_value = reMock
        reMock.match.return_value.group.return_value = 'foo,bar'
        config = MagicMock()
        config_sect_attribs = self.helper.configure_section_attributes(sections, config_data, config)
        self.assertEqual(config_sect_attribs.a, ['foo', 'bar'])
