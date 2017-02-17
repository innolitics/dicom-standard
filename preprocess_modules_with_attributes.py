'''
Performs preprocessing tasks on the module-attribute relationship JSON tables.
All of these steps are required before any further data processing can occur.
Specific processing steps are:
    1. Inline expansion of macros (preserving hierarchy markers)
    2. Expand out hierarchy markers and embed order in the attribute ID
    3. Clean up and format data fields
'''
import sys
from copy import deepcopy

from bs4 import BeautifulSoup as bs

import parse_lib as pl

def expand_macros(module_attr_tables, macro_tables):
    expanded_tables = [fill_out_macro_rows(table, macro_tables)
                        for table in module_attr_tables]
    return expanded_tables

# TODO: add heirarchy markers to newly added macro attributes.
def fill_out_macro_rows(table, macro_tables):
    expansion_locations = find_macro_expansion_locations(table)
    index_offset = 0
    for original_idx, macro_id in expansion_locations:
        idx = original_idx + index_offset
        macro_attributes = get_macro_attributes(macro_id)
        del table['attributes'][idx]
        table['attributes'][idx:idx] = macro_attributes
        index_offset += len(macro_attributes) - 1
    return table

def find_macro_expansion_locations(table):
    locations = []
    for idx, attribute_row in enumerate(table['attributes']):
        is_macro_row = attribute_row['tag'] == 'None'
        if is_macro_row:
            locations.append((idx, get_macro_id(attribute_row['name'])))
    return locations

def get_macro_id(macro_reference_html):
    parsed_reference = bs(macro_reference_html, 'html.parser')
    id_anchor = parsed_reference.find('a', class_='xref')
    return id_anchor.get('href')[1:] # Remove the first '#' character

def get_macro_attributes(macro_id):
    return macro_dict[macro_id]['attributes']

# def expand_heirarchy(tables):


# def format_table_data(tables):


if __name__ == '__main__':
    module_attr_tables = pl.read_json_to_dict(sys.argv[1])
    macro_tables = pl.read_json_to_dict(sys.argv[2])
    tables_with_macros = expand_macros(module_attr_tables, macro_tables)
    tables_with_hierarchy = expand_heirarchy(tables_with_macros)
    cleaned_tables = format_table_data(tables_with_hierarchy)
    pl.write_pretty_json(sys.argv[3], cleaned_tables)
