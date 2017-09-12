import mock
import unittest
import sys


class TestAMIMap(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch.dict('sys.modules', {'json': mock.MagicMock()})

        self.patcher.start()

        from ...providers.aws.resources import ami_map
        self.ami_map = ami_map
        self.map = self.ami_map.AMIMap('mushin', 'wobe', 'wobe_file')

    def tearDown(self):
        self.patcher.stop()

    def test_ami_map_constructor(self):
        self.assertEqual(self.map.platform, 'mushin')
        self.assertEqual(self.map.os_name, 'wobe')
        self.assertEqual(self.map.ami_file, 'wobe_file')
        self.assertEqual(self.map.ami_map, None)

    def test_ami_mappings(self):
        self.ami_map.open = mock.MagicMock()
        self.ami_map.open.return_value.__enter__.return_value = 'ami_data'
        self.ami_map.json.load.return_value = 'mymindmap'
        mappings = self.map.ami_mappings()
        self.assertEqual(mappings, 'mymindmap')
        self.ami_map.json.load.assert_called_once_with('ami_data')
        self.ami_map.open.assert_called_once_with('wobe_file')

    def test_get_ami_map_image(self):
        tmp_mappings = self.map.ami_mappings
        self.map.ami_mappings = mock.MagicMock()
        map_dict = {'mushin': {'wobe': 'omo_wobe'}}
        self.map.ami_mappings.return_value = map_dict
        ami_image = self.map.get_ami_image()
        self.assertEqual(ami_image, 'omo_wobe')
        self.map.ami_mappings.assert_called_once()
        self.map.ami_mappings = tmp_mappings
