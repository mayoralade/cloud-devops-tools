'''
Main Docker Provider class
'''
from ..provider import Provider


class DockerProvider(Provider):
    '''
        Docker Provider
    '''
    def __init__(self, config):
        super(DockerProvider, self).__init__()
        self.config = config
