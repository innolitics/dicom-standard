'''
ciod_modules.py

Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
Output the tables in JSON format, one entry per module.
'''
import sys

import parse_lib as pl

def get_ciod_module_raw(standard_path, json_path):
    pl.get_json_from_standard(standard_path, json_path, 'ciods')

if __name__ == '__main__':
    get_ciod_module_raw(sys.argv[1], sys.argv[2])
