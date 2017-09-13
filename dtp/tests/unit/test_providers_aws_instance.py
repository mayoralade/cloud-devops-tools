import mock
import unittest
import sys


class TestAWSInstance(unittest.TestCase):
    def setUp(self):
        global selfMock
        selfMock = mock.MagicMock()
        self.patcher1 = mock.patch.dict('sys.modules',
                                       {'os': mock.MagicMock(),
                                        'json': mock.MagicMock(),
                                        'dtp.helper': mock.MagicMock()})

        self.patcher1.start()

        self.patcher2 = mock.patch('dtp.providers.aws.instance.helper', mock.MagicMock())

        from ...providers.aws import instance
        self.test_instance = None
        self.module = instance
        self.patcher2.start()
        self.load_default_attributes = self.module.Instance.load_default_attributes
        self.update_attributes_from_instance = self.module.Instance.update_attributes_from_instance
        self.set_instance_attributes = self.module.Instance.set_instance_attributes
        self.module.Instance.load_default_attributes = mock.MagicMock()
        self.module.Instance.update_attributes_from_instance = mock.MagicMock()
        self.module.Instance.set_instance_attributes = mock.MagicMock()
        self.instance = self.module.Instance('mydata', 'myattribute', 'test')

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_instance_constructor(self):
        self.assertEqual(self.instance.data, 'mydata')
        self.assertEqual(self.instance.attribute_file, 'myattribute')
        self.assertEqual(self.instance.instance_name, 'test')
        self.instance.load_default_attributes.assert_called_once()
        self.instance.update_attributes_from_instance.assert_called_once()
        self.instance.set_instance_attributes.assert_called_once()

    def test_load_default_attributes(self):
        self.module.os.path.join.return_value = 'attrib'
        self.module.open = mock.MagicMock()
        self.module.open.return_value.__enter__.return_value = 'attrib_data'
        self.module.json.load.return_value = 'attrib_content'
        self.load_default_attributes(self.instance)
        self.module.open.assert_called_once_with('attrib')
        self.module.json.load.assert_called_once_with('attrib_data')
        self.assertEqual(self.instance.info, 'attrib_content')

    def test_update_attributes_from_instance(self):
        self.module.helper.flatten_dict.return_value = mock.MagicMock()
        self.update_attributes_from_instance(self.instance)
        self.assertEqual(self.module.helper.flatten_dict.call_count, 2)
        self.instance.info.update.assert_called_once()

    def test_set_instance_attributes(self):
        self.instance.info = {}
        self.set_instance_attributes(self.instance)
        self.assertEqual(self.instance.info, {'Name': 'test'})
        self.module.helper.create_attribute_from_dict.assert_called_once_with(self.instance, {'Name': 'test'})
