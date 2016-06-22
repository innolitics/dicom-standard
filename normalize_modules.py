import sys

import parse.parse_lib as pl

def normalize_modules(input_json_path, modules_output_path):
    module_attr_list = pl.read_json_to_dict(input_json_path)
    modules = module_table_from_raw_list(module_attr_list)
    pl.dump_pretty_json(modules_output_path, 'w', modules)

def module_table_from_raw_list(module_attr_list):
    modules = {}
    for module in module_attr_list:
        modules[module['name']] = {
            'slug': module['slug'],
            'link_to_standard': module['link_to_standard']
        }
    return modules


if __name__ == "__main__":
    normalize_modules(sys.argv[1], sys.argv[2])
