'''
Add the VR, VM, keyword, and retired fields to the correct attributes
by combining the attribute and property JSON files.
'''
import sys

import pandas as pd

from parse_lib import dump_pretty_json, read_json_to_dict


def extend_module_attributes(modules_with_attributes, data_element_registry):
    '''
    Given a list of DICOM modules each containing a list of DICOM attributes
    from section 3, extend the attributes with the extra properties from the DICOM data
    element registry in section 6.
    '''
    data_dictionary_dataframe = pd.DataFrame.from_dict(data_element_registry, orient='index')
    data_dictionary_dataframe.index.name = 'tag'
    for module in modules_with_attributes:
        module_attributes = module['data']
        extended_module_attributes = natural_join(data_dictionary_dataframe, module_attributes)
        module['data'] = extended_module_attributes
    return modules_with_attributes


def natural_join(data_dictionary_dataframe, raw_attributes):
    raw_attributes_dataframe = pd.DataFrame(raw_attributes)
    joined_dataframe = pd.merge(module_dataframe, raw_attributes_dataframe, left_on='tag', right_index=True)
    return joined_dataframe.to_dict(orient='records')


if __name__ == '__main__':
    modules_with_attributes = read_json_to_dict(sys.argv[1])
    data_element_registry = read_json_to_dict(sys.argv[2])

    modules_with_extended_attributes = extend_module_attributes(modules_with_attributes, data_element_registry)

    dump_pretty_json(sys.argv[3], 'w', modules_with_extended_attributes)
