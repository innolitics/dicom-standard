'''
Convert the processed macro-attribute JSON data into a
normalized listing of all macros in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl

from process_modules import modules_from_tables


if __name__ == '__main__':
    macro_attr_tables = pl.read_json_data(sys.argv[1])
    macros = modules_from_tables(macro_attr_tables, macros_only=True)
    pl.write_pretty_json(macros)
