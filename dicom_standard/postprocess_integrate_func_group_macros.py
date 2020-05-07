'''
Add functional group macro attributes to module_to_attributes.json
'''
import sys
from copy import deepcopy

import dicom_standard.parse_lib as pl
from dicom_standard.process_modules import FUNC_GROUP_MODULE_ID

PER_FRAME_FUNC_GROUP_ID = 52009230


def update_description(attribute, macro):
    note_header = '<h3>Note</h3>'
    usage = f'<p>Part of the {macro["macroName"]} Functional Group Macro with usage: {macro["usage"]}</p>'
    conditionalStatement = macro['conditionalStatement']
    if conditionalStatement and not conditionalStatement.endswith('.'):
        conditionalStatement += '.'
    conditional = f'<p>{conditionalStatement}</p>' if conditionalStatement else ''
    attribute['description'] += note_header + usage + conditional


def process_macro_attributes(macro_attrs, macro):
    attr_list = []
    for macro_attr in macro_attrs:
        attr = deepcopy(macro_attr)
        macro_id = attr.pop('macroId')
        attr['moduleId'] = f'{macro["ciodId"]}-{FUNC_GROUP_MODULE_ID}'
        new_path_prefix = f'{attr["moduleId"]}:{PER_FRAME_FUNC_GROUP_ID}'
        attr['path'] = attr['path'].replace(macro_id, new_path_prefix)
        update_description(attr, macro)
        attr_list.append(attr)
    return attr_list


def process_mffg_attributes(ciods, mffg_attrs):
    attr_list = []
    for ciod in ciods:
        module_id = f'{ciod}-{FUNC_GROUP_MODULE_ID}'
        for mffg_attr in mffg_attrs:
            attr = deepcopy(mffg_attr)
            attr['moduleId'] = module_id
            attr['path'] = attr['path'].replace(FUNC_GROUP_MODULE_ID, module_id)
            attr_list.append(attr)
    return attr_list


def process_ciod_specific_attributes(module_to_attr, macros, ciod_to_macro, macro_to_attr):
    ciod_specific_attrs = []
    macro_dict = {macro['id']: macro for macro in macros}
    for rel in ciod_to_macro:
        rel['macroName'] = macro_dict[rel['macroId']]['name']
        macro_attrs = list(filter(lambda r: r['macroId'] == rel['macroId'], macro_to_attr))
        processed_macro_attrs = process_macro_attributes(macro_attrs, rel)
        ciod_specific_attrs += processed_macro_attrs
    mffg_attrs = list(filter(lambda r: r['moduleId'] == FUNC_GROUP_MODULE_ID, module_to_attr))
    ciods_with_macros = list(set([rel['ciodId'] for rel in ciod_to_macro]))
    ciod_specific_attrs += process_mffg_attributes(ciods_with_macros, mffg_attrs)
    return ciod_specific_attrs


if __name__ == '__main__':
    module_to_attributes = pl.read_json_data(sys.argv[1])
    macros = pl.read_json_data(sys.argv[2])
    ciod_to_macro = pl.read_json_data(sys.argv[3])
    macro_to_attributes = pl.read_json_data(sys.argv[4])
    new_attributes = process_ciod_specific_attributes(module_to_attributes, macros, ciod_to_macro, macro_to_attributes)
    pl.write_pretty_json(module_to_attributes + new_attributes)
