'''
Class to manage instances
'''
import os
import json
from ... import helper


class Instance(object):
    '''
    Convert instance data to object
    '''
    def __init__(self, instance_data, attribute_file, instance_name):
        self.data = instance_data
        self.attribute_file = attribute_file
        self.instance_name = instance_name
        self.info = None
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
            self.info = json.load(def_attrib)

    def update_attributes_from_instance(self):
        '''
        Update default attributes with instance data
        '''
        self.info = helper.flatten_dict(self.info)
        self.data = helper.flatten_dict(self.data)
        self.info.update((k, v) for k, v in
                         self.data.iteritems() if k in self.info)

    def set_instance_attributes(self):
        '''
        Set Instance Attributes
        '''
        self.info['Name'] = self.instance_name
        self = helper.create_attribute_from_dict(self, self.info)
