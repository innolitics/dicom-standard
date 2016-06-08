'''
ciod_modules.py

Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
Output the tables in JSON format, one entry per module.
'''

import parse_lib as pl

def get_ciod_module_raw(standard_path, json_path):
    pl.standard_tables_to_json(standard_path, json_path, 'ciods')

if __name__ == '__main__':
    try:
        get_ciod_module_raw(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
