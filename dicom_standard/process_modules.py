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

MF_FUNC_GROUP_MODULE_ID = 'multi-frame-functional-groups'
CF_FUNC_GROUP_MODULE_ID = 'current-frame-functional-groups'


def modules_from_tables(tables):
    modules = []
    for module in tables:
        module['description'] = pl.clean_html(module['description'])
        module.pop('attributes', None)
        module.pop('isMacro', None)
        modules.append(module)
    return modules


def create_ciod_specific_modules(ciods, module, module_id):
    modules = []
    for ciod in ciods:
        ciod_specific_module = deepcopy(module)
        ciod_specific_module['id'] = f'{ciod}-{module_id}'
        modules.append(ciod_specific_module)
    return modules


if __name__ == '__main__':
    module_attr_tables = pl.read_json_data(sys.argv[1])
    ciod_to_macro = cast(List[MetadataTableType], pl.read_json_data(sys.argv[2]))
    modules = modules_from_tables(module_attr_tables)
    ciods_with_mffg_macros = list(set([rel['ciodId'] for rel in ciod_to_macro if rel['moduleType'] == 'Multi-frame']))
    ciods_with_cffg_macros = list(set([rel['ciodId'] for rel in ciod_to_macro if rel['moduleType'] == 'Current Frame']))
    multi_frame_func_group_module = next(filter(lambda rel: rel['id'] == MF_FUNC_GROUP_MODULE_ID, modules), None)
    assert multi_frame_func_group_module is not None, f'Module ID "{MF_FUNC_GROUP_MODULE_ID}" not found'
    current_frame_func_group_module = next(filter(lambda rel: rel['id'] == CF_FUNC_GROUP_MODULE_ID, modules), None)
    assert current_frame_func_group_module is not None, f'Module ID "{CF_FUNC_GROUP_MODULE_ID}" not found'
    ciod_specific_mffg_modules = create_ciod_specific_modules(ciods_with_mffg_macros, multi_frame_func_group_module, MF_FUNC_GROUP_MODULE_ID)
    ciod_specific_cffg_modules = create_ciod_specific_modules(ciods_with_cffg_macros, current_frame_func_group_module, CF_FUNC_GROUP_MODULE_ID)
    sorted_modules = sorted(modules + ciod_specific_mffg_modules + ciod_specific_cffg_modules, key=itemgetter('id'))
    pl.write_pretty_json(sorted_modules)
