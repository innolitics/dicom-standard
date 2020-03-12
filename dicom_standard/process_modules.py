'''
Convert the processed module-attribute JSON data into a
normalized listing of all modules in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl


def modules_from_tables(tables):
    modules = []
    for module in tables:
        module['description'] = pl.clean_html(module['description'])
        module.pop('attributes', None)
        modules.append(module)
    return modules


if __name__ == '__main__':
    module_attr_tables = pl.read_json_to_dict(sys.argv[1])
    modules = modules_from_tables(module_attr_tables)
    pl.write_pretty_json(modules)
