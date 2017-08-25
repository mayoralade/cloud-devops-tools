'''
Class to manage instances
'''
import os
import json
from .resources.helper import create_attribute_from_dict, flatten_dict


class Instance(object):
    '''
    Convert instance data to object
    '''
    def __init__(self, instance_data, attribute_file, instance_name):
        self.data = instance_data['Instances'][0]
        self.attribute_file = attribute_file
        self.instance_name = instance_name
        self.instance = None
        self.load_default_attributes()
        self.update_attributes_from_instance()
        self.set_instance_attributes()

    def load_default_attributes(self):
        '''
        Load default attributes from template
        '''
        attrib_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   self.attribute_file)
        with open(attrib_file) as def_attrib:
            self.instance = json.load(def_attrib)

    def update_attributes_from_instance(self):
        '''
        Update default attributes with instance data
        '''
        self.instance = flatten_dict(self.instance)
        self.data = flatten_dict(self.data)
        self.instance.update((k, v) for k, v in
                             self.data.iteritems() if k in self.instance)

    def set_instance_attributes(self):
        '''
        Set Instance Attributes
        '''
        self = create_attribute_from_dict(self, self.instance)
        setattr(self, 'Name', self.instance_name)
