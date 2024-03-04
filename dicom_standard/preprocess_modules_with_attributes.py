'''
Performs preprocessing tasks on the module-attribute relationship JSON tables.
All of these steps are required before any further data processing can occur.
Specific processing steps are:
    1. Inline expansion of macros (preserving hierarchy markers)
    2. Expand out hierarchy markers and embed order in the attribute ID
    3. Clean up and format data fields
'''
from typing import cast, Dict, List
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.macro_utils import MetadataTableType, expand_macro_rows, get_id_from_link
from dicom_standard.hierarchy_utils import record_hierarchy_for_module


def key_tables_by_id(table_list: List[MetadataTableType]) -> Dict[str, MetadataTableType]:
    return {get_id_from_link(table['linkToStandard']): table for table in table_list}


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
    table['attributes'] = [attr for attr in list(map(preprocess_attribute, table['attributes'])) if attr]
    return table


def preprocess_attribute(attr):
    return {
        'name': pl.text_from_html_string(attr['name']),
        'tag': pl.text_from_html_string(attr['tag']),
        'type': 'None' if 'type' not in attr.keys()
                else pl.text_from_html_string(attr['type']),
        'description': attr['description'],
        'conditional': attr.get('conditional'),
    }


def expand_hierarchy(tables):
    return [record_hierarchy_for_module(table) for table in tables]


if __name__ == '__main__':
    module_macro_attr_tables = cast(List[MetadataTableType], pl.read_json_data(sys.argv[1]))
    id_to_table = key_tables_by_id(module_macro_attr_tables)
    module_attr_tables = [table for table in module_macro_attr_tables if not table['isMacro']]
    expanded_tables = expand_all_macros(module_attr_tables, id_to_table)
    preprocessed_tables = preprocess_attribute_fields(expanded_tables)
    tables_with_hierarchy = expand_hierarchy(preprocessed_tables)
    pl.write_pretty_json(tables_with_hierarchy)
