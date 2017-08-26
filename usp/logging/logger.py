'''
Logging helper class
'''
import logging


class Logger(object):
    '''
    Logger Class
    '''
    def __init__(self):
        # create logger
        self.log = logging.getLogger()
        # create console handler
        self.console_handler = logging.StreamHandler()
        # set up logger
        self.setup_logger()

    def setup_logger(self):
        '''
        Configure Logger
        '''
        # set logger level to debug
        self.log.setLevel(logging.INFO)
        # set console handler level to debug
        self.console_handler.setLevel(logging.INFO)
        # create formatter
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        # add formatter to console_handler
        self.console_handler.setFormatter(formatter)
        # add console_handler to logger
        self.log.addHandler(self.console_handler)
