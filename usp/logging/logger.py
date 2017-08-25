'''
Logging helper class
'''
import logging


class Logger(object):
    '''
    Logger Class
    '''
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.format = '%(asctime)-15s %(levelname)s %(message)s'
        logging.basicConfig(format=self.format)
