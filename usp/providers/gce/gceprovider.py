'''
Main GCE Provider class
'''
from ..provider import Provider


class GCEProvider(Provider):
    '''
        GCE Provider
    '''
    def __init__(self, config):
        super(GCEProvider, self).__init__()
        self.config = config
