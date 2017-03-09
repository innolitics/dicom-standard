'''
Takes the extracted CIOD-Module table information to build a list of all
CIOD-Module relationships enumerated in the DICOM Standard.
'''
import sys
from bs4 import BeautifulSoup as bs

import parse_lib as pl

def enumerate_all_relationships(ciod_module_list):
    all_relationships = []
    for table in ciod_module_list:
        all_relationships.extend(list(map(describe_relationship_with(table['name']),
                                          table['modules'])))
    return all_relationships

def describe_relationship_with(ciod_name):
    def enumerate_relationship(module):
        usage, conditional_statement = expand_conditional_statement(module['usage'])
        return {
            "ciod": pl.create_slug(ciod_name),
            "module": pl.create_slug(pl.text_from_html_string(module['module'])),
            "usage": usage,
            "conditionalStatement": conditional_statement,
            "informationEntity": pl.text_from_html_string(module['informationEntity'])
        }
    return enumerate_relationship

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

def mark_canonical_modules(ciod_module_relationships):
    canonical_pairs = {}
    for pair in ciod_module_relationships:
        if pair['module'] not in canonical_pairs:
            canonical_pairs[pair['module']] = pair
            pair['canonical'] = True
        else:
            pair['canonical'] = False
    return ciod_module_relationships

if __name__ == '__main__':
    ciod_module_list = pl.read_json_to_dict(sys.argv[1])
    ciod_module_relationships = enumerate_all_relationships(ciod_module_list)
    ciods_modules_with_canonicals = mark_canonical_modules(ciod_module_relationships)
    pl.write_pretty_json(sys.argv[2], ciod_module_relationships)
