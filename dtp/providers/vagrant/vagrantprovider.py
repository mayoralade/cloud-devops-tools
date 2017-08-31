'''
Main Vagrant Provider class
'''
from ..provider import Provider


class VagrantProvider(Provider):
    '''
        Vagrant Provider
    '''
    def __init__(self, config):
        super(VagrantProvider, self).__init__()
        self.config = config
