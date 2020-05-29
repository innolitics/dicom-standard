'''
Load the CIOD to functional group macro tables from DICOM Standard PS3.3, Annex A.
Output the data from the tables in JSON format, one entry per CIOD.
'''
from typing import List, Tuple
import sys
import re
from copy import deepcopy

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
    table_to_dict,
)

CHAPTER_ID = 'chapter_A'
# Standard workaround: Include optional "s" at end of "Functional Group" to catch Table A.32.9-2
# http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.32.9.3.4.html#table_A.32.9-2
TABLE_SUFFIX = re.compile(".*Functional Groups? Macros$")
COLUMN_TITLES = ['macro', 'section', 'usage']


# Standard workaround: Add missing "Image" to title of Table A.52.4.3-1
# http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.52.4.3.html#table_A.52.4.3-1
def clean_macro_table_name(table_name: str) -> str:
    clean_name = pl.clean_table_name(table_name)
    if clean_name == 'Ophthalmic Tomography':
        clean_name = 'Ophthalmic Tomography Image'
    return clean_name


def is_valid_macro_table(table_div: Tag) -> bool:
    return bool(TABLE_SUFFIX.match(pr.table_name(table_div)))


def macro_table_to_dict(table: StringifiedTableListType) -> List[TableDictType]:
    return table_to_dict(table, COLUMN_TITLES)


def get_table_with_metadata(table_with_tdiv: Tuple[List[TableDictType], Tag]) -> MetadataTableType:
    table, tdiv = table_with_tdiv
    clean_name = clean_macro_table_name(pr.table_name(tdiv))
    clean_description = pl.clean_html(str(tdiv.find_previous('p')))
    module_type = 'Multi-frame' if 'Multi-frame' in clean_description \
        else 'Current Frame' if 'Current Frame' in clean_description \
        else None
    return {
        'name': clean_name,
        'macros': table,
        'id': pl.create_slug(clean_name),
        'description': clean_description,
        'linkToStandard': get_short_standard_link(tdiv),
        'moduleType': module_type,
    }


def add_enhanced_mr_color_image_table(table_data):
    ''' Standard workaround: The Enhanced MR Color Image IOD does not have its own set
    of Functional Group Macros, but instead refers to the Enhanced MR Image Functional
    Group Macros Table, so we duplicate that table object and modify the name
    See http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.36.4.4.html
    '''
    enhanced_mr_image_fg_macros = next(filter(lambda t: t['name'] == 'Enhanced MR Image', table_data), None)
    assert enhanced_mr_image_fg_macros is not None, 'Table with name "Enhanced MR Image" not found.'
    new_table = deepcopy(enhanced_mr_image_fg_macros)
    new_table['name'] = 'Enhanced MR Color Image'
    table_data.append(new_table)


if __name__ == "__main__":
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_chapter_tables(standard, CHAPTER_ID, is_valid_macro_table)
    parsed_table_data = tables_to_json(tables, tdivs, macro_table_to_dict, get_table_with_metadata)
    add_enhanced_mr_color_image_table(parsed_table_data)
    pl.write_pretty_json(parsed_table_data)
