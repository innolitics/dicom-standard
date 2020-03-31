'''
Load the macro-attribute tables from DICOM Standard PS3.3.
Output the tables in JSON format, one entry per attribute.
'''
from typing import Tuple, List
import sys
import re

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.table_utils import TableListType, tdiv_to_table_list, tables_to_json

from extract_modules_with_attributes import module_table_to_dict, get_table_with_metadata

TABLE_SUFFIX = re.compile("(.*Macro Attributes$)|(.*Macro Attributes Description$)")
COLUMN_TITLES_WITH_TYPE = ['name', 'tag', 'type', 'description']
COLUMN_TITLES_NO_TYPE = ['name', 'tag', 'description']


def get_macro_tables(standard: BeautifulSoup) -> Tuple[List[TableListType], List[Tag]]:
    all_table_divs = standard.find_all('div', class_='table')
    macro_table_divs = list(filter(is_valid_macro_table, all_table_divs))
    macro_table_lists = list(map(tdiv_to_table_list, macro_table_divs))
    return (macro_table_lists, macro_table_divs)


def is_valid_macro_table(table_div: Tag) -> bool:
    return TABLE_SUFFIX.match(pr.table_name(table_div))


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_macro_tables(standard)
    parsed_table_data = tables_to_json(tables, tdivs, module_table_to_dict, get_table_with_metadata)
    pl.write_pretty_json(parsed_table_data)
