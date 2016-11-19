import sys

import parse_lib as pl

def module_table_from_raw_list(module_attr_list):
    modules = {}
    for module in module_attr_list:
        modules[module['id']] = {
            'id': module['id'],
            'name': module['name'],
            'description': module['description'],
            'linkToStandard': module['linkToStandard']
        }
    return modules

if __name__ == "__main__":
    module_attr_list = pl.read_json_to_dict(sys.argv[1])
    modules = module_table_from_raw_list(module_attr_list)
    pl.write_pretty_json(sys.argv[2], modules)
