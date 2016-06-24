import sys

import parse.parse_lib as pl

def attributes_table_from_raw_list(attr_list, module_attr_list):
    attributes = {}
    for tag, attribute in attr_list.items():
        attributes[tag] = attribute
        attributes[tag]['slug'] = pl.create_slug(tag)
        attributes[tag]['type'] = None
        for module in module_attr_list:
            for attr in module['data']:
                if attr['tag'] == tag:
                    if attr['type'] is not None:
                        attributes[tag]['type'] = attr['type']
                        break
    return attributes

if __name__ == "__main__":
    attr_list = pl.read_json_to_dict(sys.argv[1])
    module_attr_list = pl.read_json_to_dict(sys.argv[2])
    attributes = attributes_table_from_raw_list(attr_list, module_attr_list)
    pl.dump_pretty_json(sys.argv[3], 'w', attributes)
