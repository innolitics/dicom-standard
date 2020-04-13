'''
Utility functions for expanding macros in the module-attribute
relationship tables.
'''
from typing import Any, Dict, List
import re
from copy import deepcopy

from bs4 import BeautifulSoup, Tag

from dicom_standard.hierarchy_utils import get_hierarchy_markers

AttributeType = Dict[str, str]
MetadataTableType = Dict[str, Any]
MacrosType = Dict[str, MetadataTableType]


def expand_macro_rows(table: Tag, macros: MacrosType) -> List[Dict[str, str]]:
    # This variable is used to stop an infinite macro reference
    # loop in the standard at the SR Document Content module.
    table_id = get_id_from_link(table['linkToStandard'])
    attribute_insertion_lists = [get_attributes_to_insert(attr, macros, table_id)
                                 for attr in table['attributes']]
    new_table = flatten_one_layer(attribute_insertion_lists)
    # Removes divider or stylistic rows
    return [attribute for attribute in new_table if attribute['tag'] != 'None']


def get_attributes_to_insert(attribute: AttributeType, macros: MacrosType, table_id: str) -> List[Dict[str, str]]:
    if is_macro_row(attribute):
        new_attributes = get_macro_attributes(attribute, macros, table_id)
        return new_attributes if new_attributes is not None else []
    else:
        return [attribute]


def is_macro_row(attribute: AttributeType) -> bool:
    is_abnormal_row = attribute['tag'] == 'None'
    reference_anchor_tag = BeautifulSoup(attribute['name'], 'html.parser').find('a', class_='xref')
    contains_link = reference_anchor_tag is not None
    # This line guards against a one-off reference in the standard
    # where a link actually points to prose instead of a table.
    is_table = re.match("Table.*", reference_anchor_tag.get_text()) if contains_link else False
    return bool(is_abnormal_row and contains_link and is_table)


# Note that this function *recursively expands* macro references using
# the `expand_macro_rows` function.
def get_macro_attributes(attribute: AttributeType, macros: MacrosType, table_id: str) -> List[AttributeType]:
    macro_id = referenced_macro_id_from_include_statement(attribute['name'])
    parsed_name = BeautifulSoup(attribute['name'], 'html.parser').get_text()
    hierarchy_marker = get_hierarchy_markers(parsed_name)
    if table_id != macro_id:
        return expand_macro_rows(get_macros_by_id(macro_id, macros, hierarchy_marker), macros)
    return []


def flatten_one_layer(nested_element_list: List[List[Any]]) -> List[Any]:
    return [element for element_list in nested_element_list
            for element in element_list]


def referenced_macro_id_from_include_statement(macro_reference_html: str) -> str:
    parsed_reference = BeautifulSoup(macro_reference_html, 'html.parser')
    id_anchor = parsed_reference.find('a', class_='xref')
    return id_anchor.get('href')[1:]  # Remove the first '#' character


def get_macros_by_id(macro_id: str, macros: MacrosType, hierarchy_marker: str) -> MetadataTableType:
    # A copy is required so that local modifications to attributes
    # (i.e. hierarchy marker modifications) don't persist.
    macro = deepcopy(macros[macro_id])
    macro['attributes'] = update_attribute_hierarchy_markers(macro['attributes'], hierarchy_marker)
    return macro


def update_attribute_hierarchy_markers(attributes: List[AttributeType], marker: str) -> List[AttributeType]:
    return [add_marker_to_attr(attribute, marker) for attribute in attributes]


def add_marker_to_attr(attribute: Dict[str, str], marker: str) -> Dict[str, str]:
    name_html = BeautifulSoup(attribute['name'], 'html.parser')
    parsed_attribute_name = name_html.find('td')
    if parsed_attribute_name is None:
        parsed_attribute_name = name_html.find('th')
    attribute['name'] = prepend_marker_to_attribute_name(parsed_attribute_name, marker)
    return attribute


def prepend_marker_to_attribute_name(new_attr_to_insert: Tag, marker: str) -> str:
    new_attr_to_insert.insert(0, marker)
    return str(new_attr_to_insert)


def get_id_from_link(link: str) -> str:
    _, html_id = link.split('#')
    return html_id
