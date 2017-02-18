'''
Performs preprocessing tasks on the module-attribute relationship JSON tables.
All of these steps are required before any further data processing can occur.
Specific processing steps are:
    1. Inline expansion of macros (preserving hierarchy markers)
    2. Expand out hierarchy markers and embed order in the attribute ID
    3. Clean up and format data fields
'''
import sys

import parse_lib as pl
from macro_utilities import expand_macro_rows

def expand_all_macros(module_attr_tables, macros):
    expanded_tables = [expand_macro_rows(table, macros)
                       for table in module_attr_tables]
    return expanded_tables

# def expand_hierarchy(tables):


# def format_table_data(tables):


if __name__ == '__main__':
    module_attr_tables = pl.read_json_to_dict(sys.argv[1])
    macro_tables = pl.read_json_to_dict(sys.argv[2])
    tables_with_macros = expand_all_macros(module_attr_tables, macro_tables)
    # print(tables_with_macros)
    # tables_with_hierarchy = expand_hierarchy(tables_with_macros)
    # cleaned_tables = format_table_data(tables_with_hierarchy)
    # pl.write_pretty_json(sys.argv[3], cleaned_tables)
