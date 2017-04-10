'''
Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
All CIOD tables are defined in chapter A of the DICOM Standard.
Output the tables in JSON format, one entry per CIOD.
'''
import sys
import re

import parse_lib as pl
import parse_relations as pr
from table_utils import expand_spans, table_to_dict, stringify_table, tdiv_to_table_list

CHAPTER_ID = 'chapter_A'
TABLE_SUFFIX = re.compile(".*IOD Modules$")
COLUMN_TITLES = ['informationEntity', 'module', 'reference_fragment', 'usage']

def get_ciod_tables(standard):
    chapter_A_table_divs = pl.all_tdivs_in_chapter(standard, CHAPTER_ID)
    ciod_table_divs = list(filter(is_valid_ciod_table, chapter_A_table_divs))
    ciod_table_lists = list(map(tdiv_to_table_list, ciod_table_divs))
    return (ciod_table_lists, ciod_table_divs)


def is_valid_ciod_table(table_div):
    return TABLE_SUFFIX.match(pr.table_name(table_div))


def tables_to_json(tables, tdivs):
    expanded_tables = list(map(expand_spans, tables))
    stringified_tables = map(stringify_table, expanded_tables)
    table_dicts = map(ciod_table_to_dict, stringified_tables)
    return list(map(get_table_with_metadata, zip(table_dicts, tdivs)))


def ciod_table_to_dict(table):
    return table_to_dict(table, COLUMN_TITLES)


def get_table_with_metadata(table_with_tdiv):
    table, tdiv = table_with_tdiv
    clean_name = pl.clean_table_name(pr.table_name(tdiv))
    table_description = get_ciod_description(tdiv)
    return {
        'name': clean_name,
        'modules': table,
        'id': pl.create_slug(clean_name),
        'description': str(table_description),
        'linkToStandard': get_short_standard_link(tdiv)
    }


def get_short_standard_link(tdiv):
    return pl.SHORT_DICOM_URL_PREFIX + pl.table_parent_page(tdiv) + '.html#' + pr.table_id(tdiv)


def get_ciod_description(tdiv):
    section = tdiv.parent.parent
    description_title = section.find('h3', class_='title')
    try:
        return description_title.parent.parent.parent.parent.p
    except AttributeError:
        return None

if __name__ == "__main__":
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_ciod_tables(standard)
    parsed_table_data = tables_to_json(tables, tdivs)
    pl.write_pretty_json(parsed_table_data)
