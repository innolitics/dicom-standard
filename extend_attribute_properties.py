'''
combine_attr_with_vr_vm.py
Add the VR, VM, and keyword fields to the correct attributes by combining the
attribute and vr_vm JSON files.
'''
import sys
from copy import deepcopy

import pandas as pd

from parse_lib import dump_pretty_json
from parse_lib import read_json_to_dict

def join_by_tag_attrs_and_vr_vm(standard_attrs, vr_vms):
    full_attrs = []
    vr_vm_dataframe = pd.DataFrame.from_dict(vr_vms, orient='index')
    vr_vm_dataframe.index.name = 'tag'
    for module in standard_attrs:
        new_module = {'table_name': module['table_name'], 'table_data': []}
        module_dataframe = pd.DataFrame(module['table_data']).applymap(remove_stray_newlines)
        joined_dataframe = pd.merge(module_dataframe, vr_vm_dataframe,
                                    left_on='tag', right_index=True)
        new_module['table_data'] = (joined_dataframe.to_dict(orient='records'))
        full_attrs.append(new_module)
    return full_attrs

def remove_stray_newlines(attribute_value):
    if isinstance(attribute_value, str):
        return attribute_value.replace('\n', '')
    else:
        return attribute_value

def main(standard_json_path, vr_vm_json_path, output_json_path):
    standard_attrs = read_json_to_dict(standard_json_path)
    vr_vms = read_json_to_dict(vr_vm_json_path)
    full_attrs = join_by_tag_attrs_and_vr_vm(standard_attrs, vr_vms)
    dump_pretty_json(output_json_path, 'w', full_attrs)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
