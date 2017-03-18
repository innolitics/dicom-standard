'''
Performs preprocessing tasks on the module-attribute relationship JSON tables.
All of these steps are required before any further data processing can occur.
Specific processing steps are:
    1. Inline expansion of macros (preserving hierarchy markers)
    2. Expand out hierarchy markers and embed order in the attribute ID
    3. Clean up and format data fields
'''
import sys
from typing import List, Dict, Tuple

from bs4 import BeautifulSoup
from bs4.element import PageElement

import parse_lib as pl
from macro_utils import expand_macro_rows, MacroTableType
from hierarchy_utils import record_hierarchy_for_module

def expand_all_macros(module_attr_tables: List[dict], macros: MacroTableType) -> List[dict]:
    expanded_attribute_lists = [expand_macro_rows(table, macros)
                                for table in module_attr_tables]
    return map(add_expanded_attributes_to_tables, zip(module_attr_tables, expanded_attribute_lists))

def add_expanded_attributes_to_tables(table_with_attributes: Tuple[dict, List[dict]]) -> dict:
    table, attributes = table_with_attributes
    table['attributes'] = attributes
    return table


def preprocess_attribute_fields(tables: List[dict]) -> List[dict]:
    return [preprocess_single_table(table) for table in tables]

def preprocess_single_table(table: dict) -> dict:
    table['attributes'] = list(map(preprocess_attribute, table['attributes']))
    return table

def preprocess_attribute(attr: dict) -> dict:
    cleaned_attribute = {
        'name': pl.text_from_html_string(attr['name']),
        'tag': pl.text_from_html_string(attr['tag']),
        'type': 'None' if 'type' not in attr.keys()
                else pl.text_from_html_string(attr['type']),
        'description': attr['description']
    }
    return cleaned_attribute


def expand_hierarchy(tables: List[dict]) -> List[dict]:
    return [record_hierarchy_for_module(table) for table in tables]

if __name__ == '__main__':
    module_attr_tables = pl.read_json_to_dict(sys.argv[1])
    macro_tables = pl.read_json_to_dict(sys.argv[2])
    tables_with_macros = expand_all_macros(module_attr_tables, macro_tables)
    preprocessed_tables = preprocess_attribute_fields(tables_with_macros)
    tables_with_hierarchy = expand_hierarchy(preprocessed_tables)
    pl.write_pretty_json(tables_with_hierarchy)
