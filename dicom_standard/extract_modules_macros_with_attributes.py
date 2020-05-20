'''
Load the module-attribute tables from DICOM Standard PS3.3.
Output the tables in JSON format, one entry per attribute.
'''
from typing import List, Tuple
import sys
import re

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.macro_utils import MetadataTableType
from dicom_standard.table_utils import (
    StringifiedTableListType,
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
VALID_URL_PATTERN = re.compile(r'(.*)(' + '|'.join(pl.NONSTANDARD_SECTION_IDS) + r').*(.html.*)')


def get_module_macro_tables(standard: BeautifulSoup) -> Tuple[List[TableListType], List[Tag]]:
    all_table_divs = standard.find_all('div', class_='table')
    table_divs = list(filter(is_valid_table, all_table_divs))
    table_lists = list(map(tdiv_to_table_list, table_divs))
    return (table_lists, table_divs)


def is_valid_table(table_div: Tag) -> bool:
    table_name = pr.table_name(table_div)
    return bool(TABLE_SUFFIX.match(table_name)) and 'Example' not in table_name


def module_table_to_dict(table: StringifiedTableListType) -> List[TableDictType]:
    has_type_column = len(table[0]) > 3
    column_titles = COLUMN_TITLES_WITH_TYPE if has_type_column else COLUMN_TITLES_NO_TYPE
    return table_to_dict(table, column_titles)


def fix_nonstandard_section_links(link: str) -> str:
    '''
    Standard workaround: For some reason, certain subsections are located within the base section, so return only the valid part
    Ex: C.7.16.2.5.1 should be within C.7.16.2.5, but "sect_C.7.16.2.5.html" is invalid
    The pattern has three capturing groups: anything before a nonstandard section ID, the nonstandard ID, and an instance of ".html" with anything after
    The substitution removes the extraneous subsection numbers that produce invalid links.
    "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.16.2.3.html#table_C.7.6.16-4" is replaced with
    "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.16.2.html#table_C.7.6.16-4"
    '''
    return VALID_URL_PATTERN.sub(r'\1\2\3', link)


def get_table_with_metadata(table_with_tdiv: Tuple[List[TableDictType], Tag]) -> MetadataTableType:
    table, tdiv = table_with_tdiv
    table_name = pr.table_name(tdiv)
    clean_name = pl.clean_table_name(table_name)
    table_description = pr.table_description(tdiv)
    is_macro = True if MACRO_TABLE_SUFFIX.match(table_name) else False
    # Standard workaround: Add description to module without a description paragraph
    # http://dicom.nema.org/dicom/2013/output/chtml/part03/sect_F.3.html#sect_F.3.2.1
    if table_description.has_attr('class') and 'title' in table_description.get('class'):
        table_description_str = f'<p>{clean_name} {"Macro" if is_macro else "Module"}.</p>'
        table_description = BeautifulSoup(table_description_str, 'html.parser')
    return {
        'name': clean_name,
        'attributes': table,
        'id': pl.create_slug(clean_name),
        'description': str(clean_table_description(table_description, is_macro)),
        'linkToStandard': fix_nonstandard_section_links(get_short_standard_link(tdiv)),
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
