#!/usr/bin/env python
import mock
import unittest
import sys
from StringIO import StringIO


class StatusTest(unittest.TestCase):
    def setUp(self):
        global osMockPath, jsonMock, openMock, osMockRemove, vstatDirMock, osListDirMock
        osMockPath = mock.MagicMock()
        jsonMock = mock.MagicMock()
        osMockRemove = mock.MagicMock()
        openMock = mock.MagicMock()
        vstatDirMock = mock.MagicMock()
        osListDirMock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules',
                                       {'os': mock.MagicMock(),
                                        'json': mock.MagicMock(),
                                        'open': mock.MagicMock(),
                                        'helper': mock.MagicMock()})
        self.patcher.start()

        from ... import status
        self.patcher2 = mock.patch('dtp.status.verify_status_dir', mock.MagicMock())
        self.status = status
        self.status.open = openMock
        self.status.json = jsonMock
        self.status.os.path = osMockPath
        self.status.os.remove = osMockRemove
        self.status.os.listdir = osListDirMock
        self.patcher2.start()

    def tearDown(self):
        self.patcher.stop()
        self.patcher2.stop()

    def test_create_status(self):
        self.status.open.return_value.__enter__.return_value = True
        self.status.Status.create_status('a', 'b')
        openMock.assert_called_once_with('b', 'w')
        jsonMock.dump.assert_called_once_with('a', True)

    def test_read_status(self):
        self.status.open.return_value.__enter__.return_value = False
        self.status.json.load.return_value = True
        status_read = self.status.Status.read_status('z')
        openMock.assert_called_once_with('z')
        jsonMock.load.assert_called_once_with(False)
        self.assertTrue(status_read)

    def test_update_status(self):
        self.status.Status.read_status = mock.MagicMock(spec_set=dict, return_value={})
        self.status.Status.read_status.__getitem__.side_effect = dict.__getitem__
        self.status.Status.read_status.__setitem__.side_effect = dict.__setitem__
        self.status.Status.create_status = mock.MagicMock()
        self.status.Status.update_status('a', 'b', 'c')
        self.status.Status.read_status.assert_called_once_with('a')
        self.status.Status.create_status.assert_called_once_with(
            self.status.Status.read_status.return_value, 'a')
        self.assertEqual(self.status.Status.read_status.return_value['b'], 'c')

    def test_clear_status(self):
        osMockPath.isfile.return_value = True
        self.status.Status.clear_status('a')
        osMockPath.isfile.assert_called_once_with('a')
        osMockRemove.assert_called_once_with('a')

    def test_print_all_status_with_no_dir(self):
        osListDirMock.return_value = False
        with self.assertRaises(SystemExit) as _:
            self.status.Status.print_all_status()

    def test_print_all_status_with_dir(self):
        self.status.verify_status_dir.return_value = 'dummy'
        osListDirMock.return_value = ['a']
        openMock.return_value.__enter__.return_value = True
        jsonMock.load.return_value = {'Name': 'dtp', 'State_Name': 'Good'}
        self.status.Status.print_all_status()
        output = sys.stdout.getvalue().strip('\n')
        self.assertEquals(output, '  dtp:  Good')
        osMockPath.join.assert_called_once_with('dummy', 'a')
        jsonMock.load.assert_called_once_with(True)
