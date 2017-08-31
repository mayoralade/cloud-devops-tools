'''
Class that manages all available tools
'''
import os


class DevOpsTools(object):
    '''
    Manage all devops tools
    '''
    def __init__(self, tools=None, logger=None):
        self.tools = tools
        self.logger = logger
        self.aggregate_config = ''

    def aggregate_configs(self):
        '''
        Aggregate all devops tools config
        '''
        for tool in self.tools:
            config = self.tool_config(tool)
            if not config:
                continue
            self.aggregate_config += config
            if not config.endswith('\n'):
                self.aggregate_config += '\n'
        return self.aggregate_config

    def tool_config(self, tool):
        '''
        Get data for specific devops tool
        '''
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'tools_repo/{0}.sh'.format(tool))
        try:
            with open(config_file) as cfgfn:
                return cfgfn.read()
        except IOError:
            self.logger.log.error('{0} not a recognized tool, skipping...'.format(tool))
            return

    @staticmethod
    def list_tools():
        '''
        List available tools
        '''
        print 'Available Tools:'
        for tool in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            'tools_repo')):
            print '  {0}'.format(os.path.splitext(tool)[0])
