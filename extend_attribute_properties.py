'''
Given a list of DICOM modules each containing a list of DICOM attributes
from section 3, extend the attributes with the extra properties from the DICOM data
element registry in section 6.

In particular, extend the attributes with the VR, VM, keyword, and retired fields.
'''
import sys

from parse_lib import dump_pretty_json, read_json_to_dict, left_join


def extend_module_attributes(modules_with_attributes, data_element_registry):
    for module in modules_with_attributes:
        module_attributes = module['data']
        extended_module_attributes = left_join(module_attributes, data_element_registry, 'tag')
        module['data'] = extended_module_attributes
    return modules_with_attributes


if __name__ == '__main__':
    modules_with_attributes = read_json_to_dict(sys.argv[1])
    data_element_registry = read_json_to_dict(sys.argv[2])

    modules_with_extended_attributes = extend_module_attributes(modules_with_attributes, data_element_registry)

    dump_pretty_json(sys.argv[3], 'w', modules_with_extended_attributes)
