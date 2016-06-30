import sys

import parse_lib as pl

def attributes_table_from_raw_list(attr_list, module_attr_list):
    attributes = {}
    for tag, attribute in attr_list.items():
        attributes[tag] = attribute
        attributes[tag]['slug'] = pl.create_slug(tag)
    return attributes

if __name__ == "__main__":
    attr_list = pl.read_json_to_dict(sys.argv[1])
    module_attr_list = pl.read_json_to_dict(sys.argv[2])
    attributes = attributes_table_from_raw_list(attr_list, module_attr_list)
    pl.dump_pretty_json(sys.argv[3], 'w', attributes)
