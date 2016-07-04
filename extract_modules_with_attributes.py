'''
Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''
import sys
import re

import parse_lib as pl


def module_attribute_data_from_standard(standard):
    chapter_name = "chapter_C"
    match_pattern = re.compile("(.*Module Attributes$)|(.*Module Table$)")
    column_titles = ['name', 'tag', 'type', 'description']
    column_correction = True
    return pl.table_data_from_standard(standard, chapter_name, match_pattern,
                                    column_titles, column_correction)

if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    all_modules = module_attribute_data_from_standard(standard)
    pl.write_pretty_json(sys.argv[2], all_modules)
