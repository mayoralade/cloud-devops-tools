import unittest
import mock
import sys


class TestDevOpsTools(unittest.TestCase):
    def setUp(self):
        global osMock, openMock
        osMock = mock.MagicMock()
        openMock = mock.MagicMock()
        self.patcher = mock.patch.dict('sys.modules', {
            'os': osMock
            })

        self.patcher.start()

        global TestDevOpsTools
        from ...devopstools import tools
        self.tools = tools
        self.devtools = self.tools.DevOpsTools()
        self.tools.os = osMock
        self.tools.os.path = osMock
        self.tools.open = openMock
        self.testMock = mock.MagicMock()
        self.devtools.logger = mock.MagicMock()

    def tearDown(self):
        self.patcher.stop()

    def test_aggregate_configs_no_valid_config(self):
        tmp_tool_config = self.devtools.tool_config
        self.devtools.tools = [1]
        self.devtools.tool_config = mock.MagicMock(return_value=False)
        self.assertEqual(self.devtools.aggregate_configs(), '')
        self.devtools.tool_config = tmp_tool_config

    def test_aggregate_configs_with_valid_config_no_new_line(self):
        tmp_tool_config = self.devtools.tool_config
        self.devtools.tools = [1]
        self.devtools.tool_config = mock.MagicMock(return_value='True')
        self.assertEqual(self.devtools.aggregate_configs(), 'True\n')
        self.devtools.tool_config = tmp_tool_config

    def test_aggregate_configs_with_valid_config_new_line(self):
        tmp_tool_config = self.devtools.tool_config
        self.devtools.tools = [1]
        self.devtools.tool_config = mock.MagicMock(return_value='True\n')
        self.assertEqual(self.devtools.aggregate_configs(), 'True\n')
        self.devtools.tool_config = tmp_tool_config

    def test_tool_config_with_valid_file(self):
        osMock.join.return_value = '/tmp/junk.sh'
        openMock.return_value.__enter__.return_value = self.testMock
        self.testMock.read.return_value = 'Good Data'
        self.assertEqual(self.devtools.tool_config('junk'), 'Good Data')
        openMock.assert_called_once_with('/tmp/junk.sh')

    def test_tool_config_with_invalid_file(self):
        self.devtools.logger = self.testMock
        osMock.join.return_value = '/tmp/junk.sh'
        openMock.return_value.__enter__.return_value = self.testMock
        self.testMock.read.side_effect = IOError
        self.devtools.tool_config('junk')
        openMock.assert_called_once_with('/tmp/junk.sh')
        self.devtools.logger.log.error.assert_called_once()

    def test_list_tools(self):
        self.tools.os.listdir.return_value = ['devtool']
        self.tools.os.path.splitext.return_value = ['devtool']
        self.devtools.list_tools()
        output = sys.stdout.getvalue()
        self.assertEqual(output, 'Available Tools:\n  devtool\n')
