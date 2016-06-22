import sys

import parse.parse_lib as pl

def normalize_ciod_module_relationship(input_json_path, output_json_path):
    ciod_module_list = pl.read_json_to_dict(input_json_path)
    ciod_module_relationship_list = ciod_module_relationship_table(ciod_module_list)
    pl.dump_pretty_json(output_json_path, 'w', ciod_module_relationship_list)

def ciod_module_relationship_table(ciod_module_list):
    entries = []
    for ciod in ciod_module_list:
        for module in ciod['data']:
            entries.append({
                'ciod': ciod['slug'],
                'module': pl.create_slug(module['module']),
                'usage': module['usage'],
                'conditional_statement': module['conditional_statement'],
                'order': module['order'],
                'information_entity': module['information_entity']
            })
    return entries

if __name__ == "__main__":
    normalize_ciod_module_relationship(sys.argv[1], sys.argv[2])
