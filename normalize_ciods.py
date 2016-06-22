import sys

import parse.parse_lib as pl

def normalize_ciods(input_json_path, output_json_path):
    ciod_module_list = pl.read_json_to_dict(input_json_path)
    ciods = ciod_table_from_raw_list(ciod_module_list)
    pl.dump_pretty_json(output_json_path, 'w', ciods)

def ciod_table_from_raw_list(ciod_module_list):
    ciods = {}
    for ciod in ciod_module_list:
        ciods[ciod['slug']] = {
            'description': ciod['description'],
            'link_to_standard': ciod['link_to_standard'],
            'name': ciod['name']
        }
    return ciods

if __name__ == "__main__":
    normalize_ciods(sys.argv[1], sys.argv[2])
