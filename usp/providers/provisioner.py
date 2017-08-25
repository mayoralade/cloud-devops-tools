"""
Main Provisioner class to manage all providers
"""

class Provisioner(object):
    """
        This is the main interface to all the backend providers
        available.

        This takes a provider name and config, verifies and calls
        the backend named provider
    """
    def __init__(self, provider, config):
        self.provider = provider
        self.config = config

    def verify_provider(self):
        """
            Verify the given provider is supported
        """
        pass

    def verify_config(self):
        """
            Verify the config syntax
        """
        pass

    def call_provider(self):
        """
            call the provider given with config provided
        """
        pass
