#!/usr/bin/env python
import mock
import unittest
import sys


class ProvisionerTest(unittest.TestCase):
    def setUp(self):
        global osPathMock, importModuleMock, providerMock, configMock, loggerMock, actionMock, jsonMock, openMock
        osPathMock = mock.MagicMock()
        jsonMock = mock.MagicMock()
        openMock = mock.MagicMock()
        importModuleMock = mock.MagicMock()
        providerMock = mock.MagicMock()
        configMock = mock.MagicMock()
        loggerMock = mock.MagicMock()
        actionMock = mock.MagicMock()
        self.patcher1 = mock.patch.dict('sys.modules',
                                       {'os': mock.MagicMock(),
                                        'json': mock.MagicMock(),
                                        'importlib': mock.MagicMock(),
                                        'logging': mock.MagicMock()})
        self.patcher2 = mock.patch('dtp.providers.provisioner.Logger', loggerMock)
        self.patcher1.start()

        from ...providers import provisioner
        self.provisioner = provisioner
        self.provisioner.os.path = osPathMock
        self.provisioner.open = openMock
        self.provisioner.json = jsonMock
        self.patcher2.start()
        self.cls_provisioner = self.provisioner.Provisioner(name=None,
            config=configMock, action='do_something', log_level=None)


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_verify_provider_for_invalid_provider(self):
        self.cls_provisioner.providers = ['a']
        self.cls_provisioner.config.provider = 'b'
        with self.assertRaises(SystemExit) as _:
            self.cls_provisioner.verify_provider()
        self.cls_provisioner.logger.log.error.assert_called_once()

    def test_run_command_by_provider(self):
        tmp_update_providers = self.cls_provisioner.update_providers
        tmp_verify_provider = self.cls_provisioner.verify_provider
        self.cls_provisioner.verify_providers = mock.MagicMock()
        self.cls_provisioner.update_providers = mock.MagicMock()
        self.cls_provisioner.providers = {'my_prov': 'Dummy'}
        self.cls_provisioner.config.provider = 'my_prov'
        self.provisioner.__name__ = 'test'
        self.provisioner.import_module = mock.MagicMock(return_value=importModuleMock)
        importModuleMock.Dummy = providerMock
        providerMock.return_value = providerMock.provider
        providerMock.provider.do_something = actionMock
        self.cls_provisioner.run_command_by_provider()
        self.provisioner.import_module.assert_called_once_with('..my_prov.dummy', 'test')
        providerMock.assert_called_once_with(None, configMock, loggerMock())
        actionMock.assert_called_once()
        self.cls_provisioner.update_providers = tmp_update_providers
        self.cls_provisioner.verify_provider = tmp_verify_provider

    def test_update_providers(self):
        self.provisioner.os.path.join.return_value = 'myfile'
        self.provisioner.open.return_value.__enter__.return_value = 'myjsonobject'
        self.provisioner.json.load.return_value = 'myjsondata'
        self.cls_provisioner.update_providers()
        self.provisioner.open.assert_called_once_with('myfile')
        self.provisioner.json.load.assert_called_once_with('myjsonobject')
        self.assertEqual(self.cls_provisioner.providers, 'myjsondata')
