'''
Main Azure Provider class
'''
from ..provider import Provider


class AzureProvider(Provider):
    '''
        Azure Provider
    '''
    def __init__(self, config):
        super(AzureProvider, self).__init__()
        self.config = config
