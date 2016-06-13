'''
modules_attributes.py

Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''
import sys

import parse_lib as pl

def get_module_attr_raw(standard_path, json_path):
    pl.get_json_from_standard(standard_path, json_path, 'modules')

if __name__ == '__main__':
    get_module_attr_raw(sys.argv[1], sys.argv[2])
