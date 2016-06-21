'''
extend_attribute_properties.py
Add the VR, VM, keyword, and retired fields to the correct attributes
by combining the attribute and property JSON files.
'''
import sys

import pandas as pd

from parse.parse_lib import dump_pretty_json
from parse.parse_lib import read_json_to_dict

def join_by_tag_attrs_and_properties(standard_attrs, properties):
    full_attrs = []
    properties_dataframe = pd.DataFrame.from_dict(properties, orient='index')
    properties_dataframe.index.name = 'tag'
    for module in standard_attrs:
        new_module = natural_join(properties_dataframe, module)
        full_attrs.append(new_module)
    return full_attrs

def natural_join(properties_dataframe, module):
    new_module = {'name': module['name'], 'slug': module['slug'], 'link': module['link_to_standard'], 'data': []}
    module_dataframe = pd.DataFrame(module['data'])
    joined_dataframe = pd.merge(module_dataframe, properties_dataframe,
                                left_on='tag', right_index=True)
    new_module['data'] = (joined_dataframe.to_dict(orient='records'))
    return new_module

def main(standard_json_path, properties_json_path, output_json_path):
    standard_attrs = read_json_to_dict(standard_json_path)
    properties = read_json_to_dict(properties_json_path)
    full_attrs = join_by_tag_attrs_and_properties(standard_attrs, properties)
    dump_pretty_json(output_json_path, 'w', full_attrs)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
