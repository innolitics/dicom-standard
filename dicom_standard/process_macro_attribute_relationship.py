import sys

from dicom_standard import parse_lib as pl

from process_module_attribute_relationship import get_standard_link


def macro_attr_relationship_table(macro_attr_list):
    entries = []
    for macro in macro_attr_list:
        for attribute in macro['attributes']:
            entries.append({
                'macroId': macro['id'],
                'path': attribute['id'],
                'tag': attribute['tag'],
                'type': attribute['type'],
                'linkToStandard': get_standard_link(macro, attribute),
                'description': attribute['description']
            })
    return entries


if __name__ == "__main__":
    macro_attr_list = pl.read_json_data(sys.argv[1])
    macro_attr_relationship_list = macro_attr_relationship_table(macro_attr_list)
    pl.write_pretty_json(macro_attr_relationship_list)
