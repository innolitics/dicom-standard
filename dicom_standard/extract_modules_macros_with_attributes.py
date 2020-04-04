'''
Load the module-attribute tables from DICOM Standard PS3.3.
Output the tables in JSON format, one entry per attribute.
'''
from typing import List, Match, Tuple, Union
import sys
import re

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.macro_utils import MetadataTableType
from dicom_standard.table_utils import (
    TableListType,
    TableDictType,
    tdiv_to_table_list,
    table_to_dict,
    get_short_standard_link,
    tables_to_json,
)

TABLE_SUFFIX = re.compile("(.*Module Attributes$)|(.*Module Table$)|(.*Macro Attributes$)|(.*Macro Attributes Description$)")
MACRO_TABLE_SUFFIX = re.compile("(.*Macro Attributes$)|(.*Macro Attributes Description$)")
COLUMN_TITLES_WITH_TYPE = ['name', 'tag', 'type', 'description']
COLUMN_TITLES_NO_TYPE = ['name', 'tag', 'description']


def get_module_macro_tables(standard: BeautifulSoup) -> Tuple[List[TableListType], List[Tag]]:
    all_table_divs = standard.find_all('div', class_='table')
    table_divs = list(filter(is_valid_table, all_table_divs))
    table_lists = list(map(tdiv_to_table_list, table_divs))
    return (table_lists, table_divs)


def is_valid_table(table_div: Tag) -> Union[Match, bool]:
    table_name = pr.table_name(table_div)
    return TABLE_SUFFIX.match(table_name) and 'Example' not in table_name


def module_table_to_dict(table: TableListType) -> List[TableDictType]:
    has_type_column = len(table[0]) > 3
    column_titles = COLUMN_TITLES_WITH_TYPE if has_type_column else COLUMN_TITLES_NO_TYPE
    return table_to_dict(table, column_titles)


def get_table_with_metadata(table_with_tdiv: Tuple[List[TableDictType], Tag]) -> MetadataTableType:
    table, tdiv = table_with_tdiv
    table_name = pr.table_name(tdiv)
    clean_name = pl.clean_table_name(table_name)
    table_description = pr.table_description(tdiv)
    is_macro = True if MACRO_TABLE_SUFFIX.match(table_name) else False
    return {
        'name': clean_name,
        'attributes': table,
        'id': pl.create_slug(clean_name),
        'description': str(clean_table_description(table_description, is_macro)),
        'linkToStandard': get_short_standard_link(tdiv),
        'isMacro': is_macro,
    }


def clean_table_description(description: Tag, is_macro: bool) -> Tag:
    table_link = description.find('a', class_='xref')
    if table_link is not None:
        table_link.href = ''
        table_link.name = 'span'
        table_link.string = 'This macro ' if is_macro else 'This module '
    return description


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_module_macro_tables(standard)
    parsed_table_data = tables_to_json(tables, tdivs, module_table_to_dict, get_table_with_metadata)
    pl.write_pretty_json(parsed_table_data)
