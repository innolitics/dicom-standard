import sys

import parse.parse_lib as pl

def normalize_attributes(input_json_path, attributes_output_path):
    module_attr_list = pl.read_json_to_dict(input_json_path)
    attributes = attributes_table_from_raw_list(module_attr_list)
    pl.dump_pretty_json(attributes_output_path, 'w', attributes)

def attributes_table_from_raw_list(module_attr_list):
    attributes = {}
    for module in module_attr_list:
        for attribute in module['data']:
            attributes[attribute['tag']] = {
                'name': attribute['attribute'],
                'keyword': attribute['keyword'],
                'value_representation': attribute['value_representation'],
                'value_multiplicity': attribute['value_multiplicity'],
                'type': attribute['type'],
                'description': attribute['description'],
                'parent_slug': attribute['parent_slug'],
                'slug': attribute['slug']
            }
    return attributes

if __name__ == "__main__":
    normalize_attributes(sys.argv[1], sys.argv[2])
