'''
Class that manages all available tools
'''
import os


class DevOpsTools(object):
    '''
    Manage all devops tools
    '''
    def __init__(self, tools):
        self.tools = tools
        self.aggregate_config = ''
        self.aggregate_configs()

    def aggregate_configs(self):
        '''
        Aggregate all devops tools config
        '''
        for tool in self.tools:
            config = DevOpsTools.tool_config(tool)
            self.aggregate_config += config
            if not config.endswith('\n'):
                self.aggregate_config += '\n'

    @staticmethod
    def tool_config(tool):
        '''
        Get data for specific devops tool
        '''
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'tools/{0}.sh'.format(tool))
        with open(config_file) as cfgfn:
            return cfgfn.read()
