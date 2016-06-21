'''
modules_attributes.py

Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''
import sys

import parse.parse_lib as pl

def main(standard_path, json_path):
    standard = pl.get_bs_from_html(standard_path)
    modules_json = pl.get_table_data_from_standard(standard, 'modules')
    pl.dump_pretty_json(json_path, 'w', modules_json)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
