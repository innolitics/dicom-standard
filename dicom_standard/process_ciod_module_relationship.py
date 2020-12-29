'''
Takes the extracted CIOD-Module table information to build a list of all
CIOD-Module relationships defined in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.process_modules import MF_FUNC_GROUP_MODULE_ID, CF_FUNC_GROUP_MODULE_ID


def define_all_relationships(ciod_module_list):
    all_relationships = []
    for table in ciod_module_list:
        ciod = table['name']
        modules = table['modules']
        all_relationships.extend([define_ciod_module_relationship(ciod, module)
                                  for module in modules])
    return all_relationships


def define_ciod_module_relationship(ciod, module):
    try:
        usage, conditional_statement = expand_conditional_statement(module['usage'])
    except KeyError as e:
        # TODO: Remove try/except block once missing IE column in Table A.85.1-1 is fixed (Related to Issue #17)
        if 'Common Instance Reference' in module['informationEntity']:
            # Shift every column right by one and replace missing IE column
            module['usage'] = module['referenceFragment']
            module['referenceFragment'] = module['module']
            module['module'] = module['informationEntity']
            module['informationEntity'] = "<td align=\"left\" colspan=\"1\" rowspan=\"1\">\n<p>\n<a id=\"para_040bd3bd-9a9f-4066-8431-ea1ded2a909e\" shape=\"rect\"></a>Encapsulated Document</p>\n</td>"
            usage, conditional_statement = expand_conditional_statement(module['usage'])
        else:
            raise e
    raw_information_entity = module.get('informationEntity')
    # If the "Information Entity" field doesn't exist, this is probably an single IOD rather than a CIOD, so just use the IOD name
    information_entity = pl.text_from_html_string(raw_information_entity) if raw_information_entity else ciod
    # Standard workaround: Fill in missing values in the "Information Entity" field of certain rows in Table A.32.10-1
    # http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.32.10.2.html#table_A.32.10-1
    if (ciod == 'Real-Time Video Photographic Image'
            and any(mod in module['module'] for mod in ['Real-Time Acquisition', 'Current Frame Functional Groups'])):
        # Manually input missing field
        information_entity = 'Image'
    ciod_id = pl.create_slug(ciod)
    module_id = pl.create_slug(pl.text_from_html_string(module['module']))
    # Standard workaround: Fix inconsistent capitalization in the "Information Entity" field of Rendition Selection Document
    # http://dicom.nema.org/medical/dicom/2019e/output/chtml/part03/sect_A.35.21.3.html#table_A.35.21-1
    if ciod == 'Rendition Selection Document' and module_id == 'synchronization':
        information_entity = 'Frame of Reference'
    # Create CIOD-specific "Multi-frame Functional Group" module IDs
    if module_id == MF_FUNC_GROUP_MODULE_ID:
        module_id = f'{ciod_id}-{module_id}'
    # Create CIOD-specific "Current Frame Functional Group" module IDs
    if module_id == CF_FUNC_GROUP_MODULE_ID:
        module_id = f'{ciod_id}-{module_id}'
    return {
        "ciodId": ciod_id,
        "moduleId": module_id,
        "usage": usage,
        "conditionalStatement": conditional_statement,
        "informationEntity": information_entity,
    }


def expand_conditional_statement(usage_field_html):
    usage_field = process_usage_html(usage_field_html)
    conditional_statement = extract_conditional_statement(usage_field)
    usage = usage_field[0]
    return usage, conditional_statement


def process_usage_html(usage_field_html):
    usage_field = pl.text_from_html_string(usage_field_html)
    processed_usage_field = usage_field.strip()
    if len(processed_usage_field) == 0:
        raise Exception('Empty module usage field')
    return processed_usage_field


def extract_conditional_statement(usage_field):
    if usage_field.startswith('C - '):
        conditional_statement = usage_field[4:].strip()
    elif usage_field.startswith('C') and len(usage_field) > 1:
        conditional_statement = usage_field[1:].strip()
    else:
        conditional_statement = None
    return conditional_statement


if __name__ == '__main__':
    ciod_module_list = pl.read_json_data(sys.argv[1])
    ciod_module_relationships = define_all_relationships(ciod_module_list)
    pl.write_pretty_json(ciod_module_relationships)
