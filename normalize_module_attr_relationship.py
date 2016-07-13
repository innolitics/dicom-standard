import re
import sys

import parse_lib as pl

def module_attr_relationship_table(module_attr_relationship_list):
    entries = []
    for module in module_attr_relationship_list:
        for i, attribute in enumerate(module['data']):
            entries.append({
                'module': module['id'],
                'path': (module['id'] + ':' + attribute['id']),
                'tag': attribute['tag'],
                'order': i,
                'type': attribute['type'],
                'description': attribute['description']
            })
    return entries

if __name__ == "__main__":
    module_attr_list = pl.read_json_to_dict(sys.argv[1])
    module_attr_relationship_list = module_attr_relationship_table(module_attr_list)
    pl.write_pretty_json(sys.argv[2], module_attr_relationship_list)
