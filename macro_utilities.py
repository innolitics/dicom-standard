
'''
Utility functions for expanding macros in the module-attribute
relationship tables.
'''
import re
from bs4 import BeautifulSoup as bs

import parse_lib as pl

# TODO: add heirarchy markers to newly added macro attributes.
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
    if table_id != macro_id:
        return expand_macro_rows(get_macros_by_id(macro_id, macros), macros)
    return []

def flatten(attribute_insertion_lists):
    return [attribute for insertion_list in attribute_insertion_lists
            for attribute in insertion_list]

def get_macro_id(macro_reference_html):
    parsed_reference = bs(macro_reference_html, 'html.parser')
    id_anchor = parsed_reference.find('a', class_='xref')
    return id_anchor.get('href')[1:] # Remove the first '#' character

def get_macros_by_id(macro_id, macros):
    return macros[macro_id]

def get_id_from_link(link):
    url, html_id = link.split('#')
    return html_id
