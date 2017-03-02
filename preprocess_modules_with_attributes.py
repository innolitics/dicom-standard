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
from hierarchy_utilities import get_hierarchy_markers, get_hierarchy_level, clean_field

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

def expand_hierarchy(tables):
    return [record_hierarchy_for_module(table) for table in tables]


def record_hierarchy_for_module(table):
    last_id = [table['id']]
    current_level = -1
    for attr in table['attributes']:
        last_id, current_level = update_hierarchy_position(attr, last_id, current_level)
        attr['name'] = clean_field(attr['name'])
        attr['tag'] = clean_field(attr['tag'])
        attr['id'] = ':'.join(last_id)
    return table

def update_hierarchy_position(attr, last_id, current_level):
    attr_id = pl.create_slug(clean_field(attr['name']))
    attribute_level = get_hierarchy_level(attr['name'])
    delta_l = attribute_level - current_level
    assert delta_l <= 1 # Should never skip levels
    if delta_l == 0:
        last_id[-1] = attr_id
    elif delta_l == 1:
        last_id.append(attr_id)
        current_level += 1
    elif delta_l < 0:
        last_id = last_id[:delta_l]
        last_id.append(attr_id)
        current_level += (delta_l + 1)
    return last_id, current_level


if __name__ == '__main__':
    module_attr_tables = pl.read_json_to_dict(sys.argv[1])
    macro_tables = pl.read_json_to_dict(sys.argv[2])
    tables_with_macros = expand_all_macros(module_attr_tables, macro_tables)
    preprocessed_tables = preprocess_attribute_fields(tables_with_macros)
    tables_with_hierarchy = expand_hierarchy(preprocessed_tables)
    pl.write_pretty_json(sys.argv[3], tables_with_hierarchy)
