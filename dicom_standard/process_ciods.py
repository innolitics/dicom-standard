'''
Takes the extracted CIOD information and processes it to produce a
dictionary of all CIODs in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl


def ciods_from_extracted_list(ciod_module_list):
    ciods = []
    for ciod in ciod_module_list:
        ciod['description'] = pl.clean_html(ciod['description'])
        ciod.pop('modules', None)
        ciods.append(ciod)
    return ciods


if __name__ == '__main__':
    ciod_module_list = pl.read_json_data(sys.argv[1])
    ciods = ciods_from_extracted_list(ciod_module_list)
    pl.write_pretty_json(ciods)
