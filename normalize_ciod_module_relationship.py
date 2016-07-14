import sys

import parse_lib as pl

def ciod_module_relationship_table(ciod_module_list):
    entries = []
    for ciod in ciod_module_list:
        for i, module in enumerate(ciod['data']):
            entries.append({
                'ciod': ciod['id'],
                'module': pl.create_slug(module['module']),
                'usage': module['usage'],
                'conditionalStatement': module['conditionalStatement'],
                'order': i,
                'informationEntity': module['informationEntity']
            })
    return entries

if __name__ == "__main__":
    ciod_module_list = pl.read_json_to_dict(sys.argv[1])
    ciod_module_relationship_list = ciod_module_relationship_table(ciod_module_list)
    pl.write_pretty_json(sys.argv[2], ciod_module_relationship_list)
