'''
Load the CIOD to functional group macro tables from DICOM Standard PS3.3, Annex A.
Output the data from the tables in JSON format, one entry per CIOD.
'''
from typing import List, Match, Tuple
import sys
import re

from bs4 import Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.macro_utils import MetadataTableType
from dicom_standard.table_utils import (
    TableListType,
    TableDictType,
    get_chapter_tables,
    tables_to_json,
    get_short_standard_link,
    get_table_description,
    table_to_dict,
)

CHAPTER_ID = 'chapter_A'
# Include optional "s" at end of "Functional Group" to catch Table A.32.9-2
# http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.32.9.3.4.html#table_A.32.9-2
TABLE_SUFFIX = re.compile(".*Functional Groups? Macros$")
COLUMN_TITLES = ['macro', 'section', 'usage']


# Add missing "Image" to title of Table A.52.4.3-1
# http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.52.4.3.html#table_A.52.4.3-1
def clean_macro_table_name(table_name: str) -> str:
    clean_name = pl.clean_table_name(table_name)
    if clean_name == 'Ophthalmic Tomography':
        clean_name = 'Ophthalmic Tomography Image'
    return clean_name


def is_valid_macro_table(table_div: Tag) -> Match:
    return TABLE_SUFFIX.match(pr.table_name(table_div))


def macro_table_to_dict(table: TableListType) -> List[TableDictType]:
    return table_to_dict(table, COLUMN_TITLES)


def get_table_with_metadata(table_with_tdiv: Tuple[List[TableDictType], Tag]) -> MetadataTableType:
    table, tdiv = table_with_tdiv
    clean_name = clean_macro_table_name(pr.table_name(tdiv))
    table_description = get_table_description(tdiv)
    return {
        'name': clean_name,
        'macros': table,
        'id': pl.create_slug(clean_name),
        'description': str(table_description),
        'linkToStandard': get_short_standard_link(tdiv)
    }


if __name__ == "__main__":
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_chapter_tables(standard, CHAPTER_ID, is_valid_macro_table)
    parsed_table_data = tables_to_json(tables, tdivs, macro_table_to_dict, get_table_with_metadata)
    pl.write_pretty_json(parsed_table_data)
