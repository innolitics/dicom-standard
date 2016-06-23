import sys

import parse.parse_lib as pl

def attributes_table_from_raw_list(module_attr_list):
    attributes = {}
    for module in module_attr_list:
        for attribute in module['data']:
            attributes[attribute['tag']] = attribute
    return attributes

if __name__ == "__main__":
    module_attr_list = pl.read_json_to_dict(sys.argv[1])
    attributes = attributes_table_from_raw_list(module_attr_list)
    pl.dump_pretty_json(sys.argv[2], 'w', attributes)
