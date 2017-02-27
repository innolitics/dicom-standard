'''
Performs preprocessing tasks on the module-attribute relationship JSON tables.
All of these steps are required before any further data processing can occur.
Specific processing steps are:
    1. Inline expansion of macros (preserving hierarchy markers)
    2. Expand out hierarchy markers and embed order in the attribute ID
    3. Clean up and format data fields
'''
import sys

from bs4 import BeautifulSoup

import parse_lib as pl
from macro_utilities import expand_macro_rows
from hierarchy_utilities import get_hierarchy_level

def expand_all_macros(module_attr_tables, macros):
    expanded_attribute_lists = [expand_macro_rows(table, macros)
                                for table in module_attr_tables]
    return map(add_expanded_attributes_to_tables, zip(module_attr_tables, expanded_attribute_lists))

def add_expanded_attributes_to_tables(table_with_attributes):
    table, attributes = table_with_attributes
    table['attributes'] = attributes
    return table

def preprocess_attribute_fields(tables):
    return [preprocess_single_table(table) for table in tables]

def preprocess_single_table(table):
    table['attributes'] = list(map(remove_html_of_name_and_tag, table['attributes']))
    return table

def remove_html_of_name_and_tag(attr):
    cleaned_attribute = {
        'name': BeautifulSoup(attr['name'], 'html.parser').get_text(),
        'tag': BeautifulSoup(attr['tag'], 'html.parser').get_text(),
        'description': attr['description']
    }
    return cleaned_attribute

# def expand_hierarchy(tables):

# TODO: should I extract the text from the HTML by this stage?
# def record_hierarchy_for_module(table):
#     parent = table['id']
#     previous_attr_level = 0
#     for attr in table['attributes']:


# def format_table_data(tables):



if __name__ == '__main__':
    module_attr_tables = pl.read_json_to_dict(sys.argv[1])
    macro_tables = pl.read_json_to_dict(sys.argv[2])
    tables_with_macros = expand_all_macros(module_attr_tables, macro_tables)
    preprocessed_tables = preprocess_attribute_fields(tables_with_macros)
    print(list(preprocessed_tables))
    # tables_with_hierarchy = expand_hierarchy(tables_with_macros)
    # cleaned_tables = format_table_data(tables_with_hierarchy)
    # pl.write_pretty_json(sys.argv[3], cleaned_tables)
