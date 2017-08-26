'''
Logging helper class
'''
import logging


class Logger(object):
    '''
    Logger Class
    '''
    def __init__(self, log_debug):
        # create logger
        self.log = logging.getLogger()
        # create console handler
        self.console_handler = logging.StreamHandler()
        # set up logger
        self.setup_logger(log_debug)

    def setup_logger(self, log_debug):
        '''
        Configure Logger
        '''
        # set logger level
        if log_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        self.log.setLevel(level)
        # set console handler level
        self.console_handler.setLevel(level)
        # create formatter
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        # add formatter to console_handler
        self.console_handler.setFormatter(formatter)
        # add console_handler to logger
        self.log.addHandler(self.console_handler)
