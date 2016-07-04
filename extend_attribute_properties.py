'''
Add the VR, VM, keyword, and retired fields to the correct attributes
by combining the attribute and property JSON files.
'''
import sys

import pandas as pd

from parse_lib import dump_pretty_json, read_json_to_dict


def join_by_tag_attrs_and_properties(standard_attrs, properties):
    full_attrs = []
    properties_dataframe = pd.DataFrame.from_dict(properties, orient='index')
    properties_dataframe.index.name = 'tag'
    for module in standard_attrs:
        new_module = natural_join(properties_dataframe, module)
        full_attrs.append(new_module)
    return full_attrs


def natural_join(properties_dataframe, module):
    new_module = {'name': module['name'], 'slug': module['slug'],
                  'link_to_standard': module['link_to_standard'], 'data': []}
    module_dataframe = pd.DataFrame(module['data'])
    joined_dataframe = pd.merge(module_dataframe, properties_dataframe,
                                left_on='tag', right_index=True)
    new_module['data'] = (joined_dataframe.to_dict(orient='records'))
    return new_module


if __name__ == '__main__':
    standard_attrs = read_json_to_dict(sys.argv[1])
    properties = read_json_to_dict(sys.argv[2])

    full_attrs = join_by_tag_attrs_and_properties(standard_attrs, properties)

    dump_pretty_json(sys.argv[3], 'w', full_attrs)
