import sys

import parse.parse_lib as pl

def normalize_module_attr_relationship(input_json_path, output_json_path):
    module_attr_list = pl.read_json_to_dict(input_json_path)
    module_attr_relationship_list = module_attr_relationship_table(module_attr_list)
    pl.dump_pretty_json(output_json_path, 'w', module_attr_relationship_list)

def module_attr_relationship_table(module_attr_relationship_list):
    entries = []
    for module in module_attr_relationship_list:
        for attribute in module['data']:
            entries.append({
                'module': module['slug'],
                'attribute': attribute['slug'],
                'order': attribute['order'],
            })
    return entries

if __name__ == "__main__":
    normalize_module_attr_relationship(sys.argv[1], sys.argv[2])
