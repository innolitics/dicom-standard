'''
Takes the extracted CIOD-Module table information to build a list of all
CIOD-Module relationships defined in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl


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
            module['usage'] = module['reference_fragment']
            module['reference_fragment'] = module['module']
            module['module'] = module['informationEntity']
            module['informationEntity'] = "<td align=\"left\" colspan=\"1\" rowspan=\"1\">\n<p>\n<a id=\"para_040bd3bd-9a9f-4066-8431-ea1ded2a909e\" shape=\"rect\"></a>Encapsulated Document</p>\n</td>"
            usage, conditional_statement = expand_conditional_statement(module['usage'])
        else:
            raise e
    informationEntity = pl.text_from_html_string(module['informationEntity'])
    # TODO: Remove if block once missing IE column in Table A.32.10-1 is fixed (Issue #17)
    if (not informationEntity
            and ciod == 'Real-Time Video Photographic Image'
            and any(mod in module['module'] for mod in ['Real-Time Acquisition', 'Current Frame Functional Groups'])):
        # Manually input missing field
        informationEntity = 'Image'
    return {
        "ciodId": pl.create_slug(ciod),
        "moduleId": pl.create_slug(pl.text_from_html_string(module['module'])),
        "usage": usage,
        "conditionalStatement": conditional_statement,
        "informationEntity": informationEntity
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
