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
        all_relationships.append(list(map(describe_relationship_with(table['name']), table['modules'])))

def describe_relationship_with(ciod_name):
    def enumerate_relationship(module):
        usage, conditional_statement = expand_conditional_statement(module['usage'])
        return { 
                "ciod": ciod_name,
                "module": pl.text_from_html_string(module['module']),
                "usage": usage,
                "conditionalStatement": conditional_statement, 
                "informationEntity": pl.text_from_html_string(module['informationEntity'])
               }
    return enumerate_relationship

# TODO: Improve this function (from before refactor). Too long and multifaceted.
def expand_conditional_statement(usage_field):
    stripped_usage_field = usage_field.strip()

    if len(stripped_usage_field) == 0:
        raise Exception('Empty module usage field')

    if stripped_usage_field.startswith('C - '):
        conditional_statement = stripped_usage_field[4:].strip()
    elif stripped_usage_field.startswith('C') and len(stripped_usage_field) > 1:
        conditional_statement = stripped_usage_field[1:].strip()
    else:
        conditional_statement = None

    usage = stripped_usage_field[0]
    return usage, conditional_statement

if __name__ == '__main__':
    ciod_module_list = pl.read_json_to_dict(sys.argv[1])
    ciod_module_relationships = enumerate_all_relationships(ciod_module_list)
    pl.write_pretty_json(sys.argv[2], ciod_module_relationships)
