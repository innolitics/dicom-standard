'''
modules_attributes.py

Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''

import parse_lib as pl

def get_module_attr_raw(standard_path, json_path):
    pl.standard_tables_to_json(standard_path, json_path, 'modules')

if __name__ == '__main__':
    try:
        get_module_attr_raw(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
