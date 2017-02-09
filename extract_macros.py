'''
Load the macro tables specified throughout PS3.3 in the DICOM Standard.
These tables are of the same form as the module-attribute tables and
are used to expand macro references in Annex C.
'''
import sys
import re

import parse_lib as pl
import parse_relations as pr
from table_utils import tdiv_to_table_list

# Since macro and module tables have the same form,
# we can use the same table->JSON conversion for both.
from extract_modules_with_attributes import tables_to_json

TABLE_SUFFIX = re.compile(".*Macro Attributes$")

def get_macro_tables(standard):
    all_table_divs = standard.find_all('div', class_='table')
    macro_table_divs = list(filter(is_valid_macro_table, all_table_divs))
    macro_table_lists = list(map(tdiv_to_table_list, macro_table_divs))
    return (macro_table_lists, macro_table_divs)

def is_valid_macro_table(table_div):
    return TABLE_SUFFIX.match(pr.table_name(table_div))

if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_macro_tables(standard)
    parsed_table_data = tables_to_json(tables, tdivs)
    pl.write_pretty_json(sys.argv[2], parsed_table_data)
