'''
Utility functions for expanding macros in the module-attribute
relationship tables.
'''
import re
from copy import deepcopy
from bs4 import BeautifulSoup as bs

import parse_lib as pl
from hierarchy_utilities import get_hierarchy_level

# TODO: add hierarchy markers to newly added macro attributes.
def expand_macro_rows(table, macros):
    # This variable is used to stop an infinite macro reference
    # loop in the standard at the SR Document Content module.
    table_id = get_id_from_link(table['linkToStandard'])
    attribute_insertion_lists = [get_attributes_to_insert(attr, macros, table_id)
                                 for attr in table['attributes']]
    return flatten(attribute_insertion_lists)

def get_attributes_to_insert(attribute, macros, table_id):
    if is_macro_row(attribute):
        new_attributes = get_macro_attributes(attribute, macros, table_id)
        return new_attributes if new_attributes is not None else []
    else:
        return [attribute]

def is_macro_row(attribute):
    is_abnormal_row = attribute['tag'] == 'None'
    reference_anchor_tag = bs(attribute['name'], 'html.parser').find('a', class_='xref')
    contains_link = reference_anchor_tag is not None
    # This line guards against a one-off reference in the standard
    # where a link actually points to prose instead of a table.
    is_table = re.match("Table.*", reference_anchor_tag.get_text()) if contains_link else False
    return is_abnormal_row and contains_link and is_table

# Note that this function *recursively expands* macro references using
# the `expand_macro_rows` function.
def get_macro_attributes(attribute, macros, table_id):
    macro_id = referenced_macro_id_from_include_statement(attribute['name'])
    hierarchy_level = get_include_markers_from_include(attribute['name'])
    if table_id != macro_id:
        return expand_macro_rows(get_macros_by_id(macro_id, macros, hierarchy_level), macros)
    return []

def get_include_markers_from_include(include_html):
    parsed_include = bs(include_html, 'html.parser')
    return get_hierarchy_level(parsed_include.get_text().strip())

def flatten(attribute_insertion_lists):
    return [attribute for insertion_list in attribute_insertion_lists
            for attribute in insertion_list]

def referenced_macro_id_from_include_statement(macro_reference_html):
    parsed_reference = bs(macro_reference_html, 'html.parser')
    id_anchor = parsed_reference.find('a', class_='xref')
    return id_anchor.get('href')[1:] # Remove the first '#' character

def get_macros_by_id(macro_id, macros, hierarchy_level):
    # A copy is required so that local modifications to attributes
    # (i.e. hierarchy marker modifications) don't persist.
    macro = deepcopy(macros[macro_id])
    macro['attributes'] = update_attribute_hierarchy_levels(macro['attributes'], hierarchy_level)
    return macro

def update_attribute_hierarchy_levels(attributes, level):
    return [add_level_to_attr(attribute, level) for attribute in attributes]

def add_level_to_attr(attribute, level):
    parsed_attribute_name = bs(attribute['name'], 'html.parser').find('td')
    attribute['name'] = prepend_level_to_attribute_name(parsed_attribute_name, level)
    return attribute

def prepend_level_to_attribute_name(new_attr_to_insert, level):
    new_attr_to_insert.insert(0, level)
    return str(new_attr_to_insert)

def get_id_from_link(link):
    url, html_id = link.split('#')
    return html_id
