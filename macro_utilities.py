'''
Utility functions for expanding macros in the module-attribute
relationship tables.
'''
import re
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
    macro_id = get_macro_id(attribute['name'])
    hierarchy_level = get_level_of_include(attribute['name'])
    if table_id != macro_id:
        return expand_macro_rows(get_macros_by_id(macro_id, macros, hierarchy_level), macros)
    return []

def get_level_of_include(include_html):
    parsed_include = bs(include_html, 'html.parser')
    return get_hierarchy_level(parsed_include.get_text().strip())

def flatten(attribute_insertion_lists):
    return [attribute for insertion_list in attribute_insertion_lists
            for attribute in insertion_list]

def get_macro_id(macro_reference_html):
    parsed_reference = bs(macro_reference_html, 'html.parser')
    id_anchor = parsed_reference.find('a', class_='xref')
    return id_anchor.get('href')[1:] # Remove the first '#' character

def get_macros_by_id(macro_id, macros, hierarchy_level):
    macro = macros[macro_id]
    # print(hierarchy_level)
    macro['attributes'] = update_attribute_hierarchy_levels(macro['attributes'], hierarchy_level)
    return macro

def update_attribute_hierarchy_levels(attributes, level):
    return [append_level_to_attr(attribute, level) for attribute in attributes]

def append_level_to_attr(attribute, level):
    # print(attribute['name'])
    parsed_attribute_name = bs(attribute['name'], 'html.parser').find('p')
    # print(parsed_attribute_name.string)
    # TODO: Modify the attribute name while retaining integrity of HTML?
    # Is this actually necessary, or are we done with the HTML information
    # in the name field?
    parsed_attribute_name.string = level + parsed_attribute_name.string
    attribute['name'] = str(parsed_attribute_name)
    return attribute

def get_id_from_link(link):
    url, html_id = link.split('#')
    return html_id
