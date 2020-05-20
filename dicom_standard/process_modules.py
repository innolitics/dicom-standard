'''
Convert the processed module-attribute JSON data into a
normalized listing of all modules in the DICOM Standard.
'''
from typing import cast, List
import sys
from copy import deepcopy
from operator import itemgetter

from dicom_standard import parse_lib as pl
from dicom_standard.macro_utils import MetadataTableType

FUNC_GROUP_MODULE_ID = 'multi-frame-functional-groups'


def modules_from_tables(tables):
    modules = []
    for module in tables:
        module['description'] = pl.clean_html(module['description'])
        module.pop('attributes', None)
        module.pop('isMacro', None)
        modules.append(module)
    return modules


def create_ciod_specific_modules(ciods, mffg_module):
    modules = []
    for ciod in ciods:
        ciod_specific_module = deepcopy(mffg_module)
        ciod_specific_module['id'] = f'{ciod}-{FUNC_GROUP_MODULE_ID}'
        modules.append(ciod_specific_module)
    return modules


if __name__ == '__main__':
    module_attr_tables = pl.read_json_data(sys.argv[1])
    ciod_to_macro = cast(List[MetadataTableType], pl.read_json_data(sys.argv[2]))
    modules = modules_from_tables(module_attr_tables)
    ciods_with_macros = list(set([rel['ciodId'] for rel in ciod_to_macro]))
    multi_frame_func_group_module = next(filter(lambda rel: rel['id'] == FUNC_GROUP_MODULE_ID, modules), None)
    assert multi_frame_func_group_module is not None, f'Module ID "{FUNC_GROUP_MODULE_ID}" not found in modules.json'
    ciod_specific_modules = create_ciod_specific_modules(ciods_with_macros, multi_frame_func_group_module)
    sorted_modules = sorted(modules + ciod_specific_modules, key=itemgetter('id'))
    pl.write_pretty_json(sorted_modules)
