'''
Main USP Interface
'''
#from .options import CommandlineOptions
import os
import sys
from shutil import copy2
from argparse import Namespace
from . import helper
from .providers.provisioner import Provisioner
from .devopstools.tools import DevOpsTools
from .status import Status


def construct_config_path(config_path, config_name):
    '''
    Construct config file path from path and config name
    '''
    return '{0}.cfg'.format(os.path.join(config_path, config_name))

def copy_config_template(resource_path):
    '''
    Copy config file template to user home directory
    '''
    template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'sample/sample_configuration.cfg')
    user_template_file = os.path.join(resource_path, 'sample_configuration.cfg')
    if os.path.isfile(user_template_file):
        msg = '''
        Create a default configuration file to use <dtp_default.cfg> for instances
        without any configuration file. <sample_configuration.cfg> already exists in
        your home directory.
        '''
        sys.exit('ERROR: {0}'.format(msg))
    copy2(template_file, resource_path)

def load_config_files(given_config, default_config):
    '''
    Load config files to be used to provision instance
    '''
    resource_path = os.path.expanduser('~')
    default_cfg_file = construct_config_path(resource_path, default_config)
    given_cfg_file = construct_config_path(resource_path, given_config)
    if os.path.isfile(given_cfg_file):
        return given_cfg_file
    elif os.path.isfile(default_cfg_file):
        return default_cfg_file
    else:
        msg = ''''A default template file <sample_configuration.cfg> has been
        created in your home dir, please modify this file, rename it to
        <dtp_default.cfg> and all other instances not having a config file tied to
        it will use the provider specified under the [resource] section'''
        copy_config_template(resource_path)
        sys.exit('ERROR: {0}'.format(msg))

def define_config_attributes(resource_name):
    '''
    Define resource configuration attributes
    '''
    config_file = load_config_files(resource_name, 'dtp_default')
    config_data = helper.load_config_file(config_file)
    provider = config_data.get('resource', 'provider')
    return helper.configure_section_attributes(['resource', provider, 'services'],
                                               config_data,
                                               Namespace())

def manage_resource(name, config, action, log_level):
    '''
    Manage resource by action given
    '''
    provisioner = Provisioner(name, config, action, log_level)
    provisioner.run_command_by_provider()

def run_command(args):
    '''
    Run requested action
    '''
    if args.action == 'list':
        if args.name == 'tools':
            DevOpsTools.list_tools()
        elif args.name in ('instances', 'vms', 'boxes'):
            Status.print_all_status()
        else:
            sys.exit('ERROR: please use "list" with <tools|instances|vms|boxes>')
    else:
        config = define_config_attributes(args.name)
        manage_resource(args.name, config, args.action, args.debug)
