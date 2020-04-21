'''
Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
All CIOD tables are defined in chapter A of the DICOM Standard.
Output the tables in JSON format, one entry per CIOD.
'''
from typing import List, Tuple
import sys
import re

from bs4 import Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.macro_utils import MetadataTableType
from dicom_standard.table_utils import (
    StringifiedTableListType,
    TableDictType,
    get_chapter_tables,
    tables_to_json,
    get_short_standard_link,
    get_table_description,
    table_to_dict,
)

CHAPTER_IDS = ['chapter_A', 'chapter_F']
# Standard workaround: Include upper case "S" to catch typo in Table A.39.19-1
# http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.35.19.3.html
TABLE_SUFFIX = re.compile(".*IOD Module[sS]$")
COLUMN_TITLES_WITH_IE = ['informationEntity', 'module', 'referenceFragment', 'usage']
COLUMN_TITLES_NO_IE = ['module', 'referenceFragment', 'usage', 'description']


def is_valid_ciod_table(table_div: Tag) -> bool:
    return bool(TABLE_SUFFIX.match(pr.table_name(table_div)))


def ciod_table_to_dict(table: StringifiedTableListType) -> List[TableDictType]:
    # Table F.3-1 (the only table in section F) has no "Information Entity" column, so we check for the href in the second column
    # http://dicom.nema.org/dicom/2013/output/chtml/part03/sect_F.3.html#table_F.3-1
    sect_f_table = 'href' in table[0][1]
    column_titles = COLUMN_TITLES_NO_IE if sect_f_table else COLUMN_TITLES_WITH_IE
    return table_to_dict(table, column_titles)


def get_table_with_metadata(table_with_tdiv: Tuple[List[TableDictType], Tag]) -> MetadataTableType:
    table, tdiv = table_with_tdiv
    clean_name = pl.clean_table_name(pr.table_name(tdiv))
    table_description = get_table_description(tdiv)
    return {
        'name': clean_name,
        'modules': table,
        'id': pl.create_slug(clean_name),
        'description': str(table_description),
        'linkToStandard': get_short_standard_link(tdiv)
    }


if __name__ == "__main__":
    standard = pl.parse_html_file(sys.argv[1])
    tables = []
    tdivs = []
    for chapter_id in CHAPTER_IDS:
        chapter_tables, chapter_tdivs = get_chapter_tables(standard, chapter_id, is_valid_ciod_table)
        tables += chapter_tables
        tdivs += chapter_tdivs
    parsed_table_data = tables_to_json(tables, tdivs, ciod_table_to_dict, get_table_with_metadata)
    pl.write_pretty_json(parsed_table_data)
