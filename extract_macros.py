'''
Load the macro tables specified throughout PS3.3 in the DICOM Standard.
These tables are of the same form as the module-attribute tables and
are used to expand macro references in Annex C.
'''
import sys
import re

import parse_lib as pl
import parse_relations as pr
from table_utils import expand_spans, table_to_dict, stringify_table, tdiv_to_table_list
from macro_utils import get_id_from_link

# Macros and modules require the same metadata and formatting,
# so they can share these two functions.
from extract_modules_with_attributes import module_table_to_dict, get_table_with_metadata

# TODO: change regex syntax to r'' instead of re.compile()?
TABLE_SUFFIX = re.compile("(.*Macro Attributes$)|(.*Macro Attributes Description$)")

def get_macro_tables(standard):
    all_table_divs = standard.find_all('div', class_='table')
    macro_table_divs = list(filter(is_valid_macro_table, all_table_divs))
    macro_table_lists = list(map(tdiv_to_table_list, macro_table_divs))
    return (macro_table_lists, macro_table_divs)

def is_valid_macro_table(table_div):
    return TABLE_SUFFIX.match(pr.table_name(table_div))


def tables_to_json(tables, tdivs):
    expanded_tables = list(map(expand_spans, tables))
    stringified_tables = map(stringify_table, expanded_tables)
    table_dicts = map(module_table_to_dict, stringified_tables)
    list_of_tables = list(map(get_table_with_metadata, zip(table_dicts, tdivs)))
    return key_tables_by_id(list_of_tables)

def key_tables_by_id(list_of_tables):
    dict_of_tables = {}
    for table in list_of_tables:
        dict_of_tables[get_id_from_link(table['linkToStandard'])] = table
    return dict_of_tables


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_macro_tables(standard)
    parsed_table_data = tables_to_json(tables, tdivs)
    pl.write_pretty_json(sys.argv[2], parsed_table_data)
