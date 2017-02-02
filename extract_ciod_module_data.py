'''
Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
All CIOD tables are defined in chapter A of the DICOM Standard.
Output the tables in JSON format, one entry per CIOD.
'''
import sys
import re

from parse_lib import parse_html_file, write_pretty_json, all_tdivs_in_chapter
from table_utils import expand_spans
from parse_relations import table_rows, table_name

CIOD_CHAPTER_ID = 'chapter_A'
CIOD_TABLE_SUFFIX = re.compile(".*IOD Modules$")

def get_ciod_tables(standard):
    chapter_A_table_divs = all_tdivs_in_chapter(standard, CIOD_CHAPTER_ID)
    ciod_table_divs = filter(is_valid_ciod_table, chapter_A_table_divs)
    ciod_table_lists = list(map(tdiv_to_table_list, ciod_table_divs))
    return ciod_table_lists

def is_valid_ciod_table(table_div):
    return CIOD_TABLE_SUFFIX.match(table_name(table_div))

def tdiv_to_table_list(table_div):
    rows = table_rows(table_div)
    table = [tr_to_row_list(row) for row in rows]
    return table

def tr_to_row_list(tr):
    row_cells = tr.find_all('td')
    cells = [str(cell) for cell in row_cells]
    return add_empty_cells(cells)

def add_empty_cells(cells):
    for i in range(len(cells), 4):
        cells.append(None)
    return cells


def tables_to_json(tables):
    expanded_tables = map(expand_spans, tables)
    # TODO: format the expanded tables into the appropriate JSON structure.

if __name__ == "__main__":
    standard = parse_html_file(sys.argv[1])
    tables = get_ciod_tables(standard)
    parsed_table_data = tables_to_json(tables)
    write_pretty_json(sys.argv[2], parsed_table_data)
