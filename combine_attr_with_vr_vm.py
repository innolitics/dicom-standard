'''
combine_attr_with_vr_vm.py
Add the VR, VM, and keyword fields to the correct attributes by combining the
attribute and vr_vm JSON files. 
'''
import sys
import json
from copy import deepcopy

def combine_attr_and_vr_vm(attribute_json_path, vr_vm_json_path, output_json_path):
    standard_attrs, vr_vms = get_json_objects(attribute_json_path, vr_vm_json_path)
    full_attrs = []
    for module in standard_attrs:
        new_module = { 'table_name': module['table_name'], 'table_data': [] }
        for attr in module['table_data']:
            new_attr = append_new_fields_to_json(attr, vr_vms)
            if new_attr is None:
                continue
            new_module['table_data'].append(new_attr)
        full_attrs.append(new_module)
    with open(output_json_path, 'w') as output_json_complete:
        output_json_complete.write(json.dumps(full_attrs, sort_keys=False, indent=4, separators=(',',':')) + "\n")

def get_json_objects(attribute_json_path, vr_vm_json_path):
    with open(attribute_json_path, 'r') as attr_file, open(vr_vm_json_path, 'r') as vr_vm_file:
        attr_string = attr_file.read()
        vr_vm_string = vr_vm_file.read()
        standard_attrs = json.loads(attr_string)
        vr_vms = json.loads(vr_vm_string)
        return standard_attrs, vr_vms

def find_tag_in_vr_vm_table(tag, vr_vms):
    for attr in vr_vms["table_data"]:
        if attr["tag"] == tag:
            return attr
    raise ValueError("Tag not found in Section 6!")

def append_new_fields_to_json(old_attr, vr_vms):
    tag = old_attr["tag"].replace('\n', '')
    new_attr = deepcopy(old_attr)
    try:
        vr_vm_entry = find_tag_in_vr_vm_table(tag, vr_vms)
    except ValueError:
        return None 
    new_attr["vr"] = vr_vm_entry["vr"]
    new_attr["vm"] = vr_vm_entry["vm"]
    new_attr["keyword"] = vr_vm_entry["keyword"]
    return new_attr

if __name__ == '__main__':
    try:
        combine_attr_and_vr_vm(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
