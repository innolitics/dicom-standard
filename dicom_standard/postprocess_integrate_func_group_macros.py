'''
Add functional group macro attributes to module_to_attributes.json
'''
import sys
from copy import deepcopy
from operator import itemgetter

import dicom_standard.parse_lib as pl
from dicom_standard.process_modules import MF_FUNC_GROUP_MODULE_ID, CF_FUNC_GROUP_MODULE_ID

SHARED_FUNC_GROUP_ID = '52009229'
PER_FRAME_FUNC_GROUP_ID = '52009230'
CURRENT_FRAME_FUNC_GROUP_ID = '00060001'


def update_description(attribute, macro):
    note_header = '<h3>Note</h3>'
    usage = f'<p>Part of the {macro["macroName"]} Functional Group Macro with usage: {macro["usage"]}</p>'
    conditionalStatement = macro['conditionalStatement']
    if conditionalStatement and not conditionalStatement.endswith('.'):
        conditionalStatement += '.'
    conditional = f'<p>{conditionalStatement}</p>' if conditionalStatement else ''
    attribute['description'] += note_header + usage + conditional


def convert_macro_attr(macro_attr, macro, fg_attr_id):
    attr = deepcopy(macro_attr)
    macro_id = attr.pop('macroId')
    fg_module_id = CF_FUNC_GROUP_MODULE_ID if fg_attr_id == CURRENT_FRAME_FUNC_GROUP_ID else MF_FUNC_GROUP_MODULE_ID
    attr['moduleId'] = f'{macro["ciodId"]}-{fg_module_id}'
    new_path_prefix = f'{attr["moduleId"]}:{fg_attr_id}'
    attr['path'] = attr['path'].replace(macro_id, new_path_prefix)
    update_description(attr, macro)
    return attr


def process_mffg_macro_attributes(macro_attrs, macro):
    attr_list = []
    for macro_attr in macro_attrs:
        attr_list.append(convert_macro_attr(macro_attr, macro, SHARED_FUNC_GROUP_ID))
        attr_list.append(convert_macro_attr(macro_attr, macro, PER_FRAME_FUNC_GROUP_ID))
    return attr_list


def process_cffg_macro_attributes(macro_attrs, macro):
    return [convert_macro_attr(macro_attr, macro, CURRENT_FRAME_FUNC_GROUP_ID) for macro_attr in macro_attrs]


def process_fg_attributes(module_to_attr, ciods, fg_module_id):
    fg_attrs = list(filter(lambda r: r['moduleId'] == fg_module_id, module_to_attr))
    attr_list = []
    for ciod in ciods:
        module_id = f'{ciod}-{fg_module_id}'
        for fg_attr in fg_attrs:
            attr = deepcopy(fg_attr)
            attr['moduleId'] = module_id
            attr['path'] = attr['path'].replace(fg_module_id, module_id)
            attr_list.append(attr)
    return attr_list


def process_ciod_specific_attributes(module_to_attr, macros, ciod_to_macro, macro_to_attr):
    ciod_specific_attrs = []
    macro_dict = {macro['id']: macro for macro in macros}
    for rel in ciod_to_macro:
        rel['macroName'] = macro_dict[rel['macroId']]['name']
        macro_attrs = list(filter(lambda r: r['macroId'] == rel['macroId'], macro_to_attr))
        module_type = rel['moduleType']
        if module_type == 'Multi-frame':
            processed_macro_attrs = process_mffg_macro_attributes(macro_attrs, rel)
        elif module_type == 'Current Frame':
            processed_macro_attrs = process_cffg_macro_attributes(macro_attrs, rel)
        else:
            raise Exception(f'Module type property should be either "Multi-frame" or "Current Frame" but is {module_type}, {rel}')
        ciod_specific_attrs += processed_macro_attrs
    # Create CIOD-specific versions of each non-macro attribute within the relevant modules
    ciods_with_mffg_macros = list(set([rel['ciodId'] for rel in ciod_to_macro if rel['moduleType'] == 'Multi-frame']))
    ciod_specific_attrs += process_fg_attributes(module_to_attr, ciods_with_mffg_macros, MF_FUNC_GROUP_MODULE_ID)
    ciods_with_cffg_macros = list(set([rel['ciodId'] for rel in ciod_to_macro if rel['moduleType'] == 'Current Frame']))
    ciod_specific_attrs += process_fg_attributes(module_to_attr, ciods_with_cffg_macros, CF_FUNC_GROUP_MODULE_ID)
    return ciod_specific_attrs


if __name__ == '__main__':
    module_to_attributes = pl.read_json_data(sys.argv[1])
    macros = pl.read_json_data(sys.argv[2])
    ciod_to_macro = pl.read_json_data(sys.argv[3])
    macro_to_attributes = pl.read_json_data(sys.argv[4])
    new_attributes = process_ciod_specific_attributes(module_to_attributes, macros, ciod_to_macro, macro_to_attributes)
    sorted_modules_to_attributes = sorted(module_to_attributes + new_attributes, key=itemgetter('path'))
    pl.write_pretty_json(sorted_modules_to_attributes)
