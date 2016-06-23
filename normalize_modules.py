import sys

import parse.parse_lib as pl

def module_table_from_raw_list(module_attr_list):
    modules = {}
    for module in module_attr_list:
        modules[module['slug']] = {
            'name': module['name'],
            'link_to_standard': module['link_to_standard']
        }
    return modules

if __name__ == "__main__":
    module_attr_list = pl.read_json_to_dict(sys.argv[1])
    modules = module_table_from_raw_list(module_attr_list)
    pl.dump_pretty_json(sys.argv[2], 'w', modules)
