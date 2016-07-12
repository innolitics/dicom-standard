import sys

import parse_lib as pl

def ciod_table_from_raw_list(ciod_module_list):
    ciods = {}
    for ciod in ciod_module_list:
        ciods[ciod['id']] = {
            'description': ciod['description'].strip(),
            'linkToStandard': ciod['linkToStandard'],
            'name': ciod['name']
        }
    return ciods

if __name__ == "__main__":
    ciod_module_list = pl.read_json_to_dict(sys.argv[1])
    ciods = ciod_table_from_raw_list(ciod_module_list)
    pl.write_pretty_json(sys.argv[2], ciods)
