'''
Takes the extracted CIOD information and processes it to produce a
dictionary of all CIODs in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl


def ciods_from_extracted_list(ciod_module_list, ciod_to_uid):
    ciods = {}
    for ciod in ciod_module_list:
        ciod_id = ciod['id']
        ciods[ciod_id] = {
            'id': ciod_id,
            'description': pl.clean_html(ciod['description']),
            'linkToStandard': ciod['linkToStandard'],
            'name': ciod['name'],
            'uid': ciod_to_uid[ciod_id] if ciod_id in ciod_to_uid else ''
        }
    return ciods


if __name__ == '__main__':
    ciod_module_list = pl.read_json_to_dict(sys.argv[1])
    ciod_to_uid = pl.read_json_to_dict(sys.argv[2])
    ciods = ciods_from_extracted_list(ciod_module_list, ciod_to_uid)
    pl.write_pretty_json(ciods)
