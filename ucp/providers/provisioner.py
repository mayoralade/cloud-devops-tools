"""
Main Provisioner class to manage all providers
"""
import os
import sys
import json
from importlib import import_module
from ..logging.logger import Logger


class Provisioner(object):
    """
        This is the main interface to all the backend providers
        available.

        This takes a provider name and config, verifies and calls
        the backend named provider
    """
    def __init__(self, name, config, action, log_level):
        self.name = name
        self.config = config
        self.action = action
        self.providers = None
        self.logger = Logger(log_level)
        self.update_providers()

    def verify_provider(self):
        """
            Verify the given provider is supported
        """
        if self.config.provider not in self.providers:
            self.logger.log.error('Provider: %s not currently supported', self.config.provider)
            sys.exit(1)

    def run_command_by_provider(self):
        """
            call the provider given with config provided
        """
        self.verify_provider()
        provider_name = self.providers[self.config.provider]
        module_name = '..{0}.{1}'.format(self.config.provider,
                                         provider_name.lower())
        module = import_module(module_name, __name__)
        provider = getattr(module, self.providers[self.config.provider])
        provider = provider(self.name, self.config, self.logger)
        action = getattr(provider, self.action)
        action()

    def update_providers(self):
        '''
        Load Provider Map
        '''
        provider_map_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                         'provider_maps.json')
        with open(provider_map_file) as pmfile:
            self.providers = json.load(pmfile)
