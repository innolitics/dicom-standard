'''
Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Output the tables in JSON format, one entry per attribute.
'''
import sys
import re

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.table_utils import (get_chapter_tables, tables_to_json,
    get_short_standard_link, table_to_dict)

CHAPTER_ID = 'chapter_C'
TABLE_SUFFIX = re.compile("(.*Module Attributes$)|(.*Module Table$)")
COLUMN_TITLES_WITH_TYPE = ['name', 'tag', 'type', 'description']
COLUMN_TITLES_NO_TYPE = ['name', 'tag', 'description']


def is_valid_module_table(table_div):
    return TABLE_SUFFIX.match(pr.table_name(table_div))


def module_table_to_dict(table):
    has_type_column = len(table[0]) > 3
    column_titles = COLUMN_TITLES_WITH_TYPE if has_type_column else COLUMN_TITLES_NO_TYPE
    return table_to_dict(table, column_titles)


def get_table_with_metadata(table_with_tdiv):
    table, tdiv = table_with_tdiv
    clean_name = pl.clean_table_name(pr.table_name(tdiv))
    table_description = pr.table_description(tdiv)
    return {
        'name': clean_name,
        'attributes': table,
        'id': pl.create_slug(clean_name),
        'description': str(clean_table_description(table_description)),
        'linkToStandard': get_short_standard_link(tdiv)
    }


def clean_table_description(description):
    table_link = description.find('a', class_='xref')
    if table_link is not None:
        table_link.href = ''
        table_link.name = 'span'
        table_link.string = 'This module '
    return description


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_chapter_tables(standard, CHAPTER_ID, is_valid_module_table)
    parsed_table_data = tables_to_json(tables, tdivs, module_table_to_dict, get_table_with_metadata)
    pl.write_pretty_json(parsed_table_data)
