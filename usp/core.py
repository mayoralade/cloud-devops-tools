'''
Main USP Interface
'''
#from .options import CommandlineOptions
import os
from argparse import Namespace, ArgumentParser
from . import helper
from .providers.provisioner import Provisioner


def load_system_config():
    '''
    Load system configutation file
    '''
    sys_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'usp.cfg')
    sys_config = helper.load_config_file(sys_config_path)
    return sys_config

def load_resource_config(resource_name):
    '''
    Load resource configuration file
    '''
    sys_config = load_system_config()
    resource_config_path = sys_config.get('defaults', 'machine_config_dir')
    resource_config = helper.load_config_file('{0}{1}.cfg'.format(resource_config_path,
                                                                  resource_name))
    provider = resource_config.get('resource', 'provider')
    config = Namespace()
    for name, value in resource_config.items(provider):
        if ',' in value:
            value = [int(i) for i in value.split(',')]
        setattr(config, name, value)
    setattr(config, 'provider', provider)
    return config

def manage_resource(config, action, log_level):
    '''
    Manage resource by action given
    '''
    provisioner = Provisioner(config, action, log_level)
    provisioner.run_command_by_provider()

def run_command(name, action, log_level):
    '''
    Run requested action
    '''
    config = load_resource_config(name)
    manage_resource(config, action, log_level)

def main():
    '''
    Main Program
    '''
    parser = ArgumentParser(prog='usp', usage='%(prog)s <action> <name>')
    parser.add_argument('action', choices=['create', 'start', 'login', 'halt', 'destroy', 'status'],
                        help='action required')
    parser.add_argument('name', help='Name of resource to create, matching config file')
    parser.add_argument('--debug', '-d', action='store_true', help='Set logging level to debug')
    args = parser.parse_args()
    run_command(args.name, args.action, args.debug)

if __name__ == '__main__':
    main()
