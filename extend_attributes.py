'''
Extend the list of DICOM attributes with the extra properties from the DICOM data
element registry in section 6.

In particular, extend the attributes with the VR, VM, keyword, and retired fields.
'''
import sys

from parse_lib import write_pretty_json, read_json_to_dict


def left_join(left_table, right_table, key):
    joined = {}
    for key, left_row in left_table.items():
        try:
            right_row = right_table[key]
            joined[key] = {**left_row, **right_row}
        except KeyError as e:
            print(key)
            print(left_row)
            raise e
    return joined


if __name__ == '__main__':
    attributes = read_json_to_dict(sys.argv[1])
    data_element_registry = read_json_to_dict(sys.argv[2])
    extended_attributes = left_join(attributes, data_element_registry, 'tag')
    write_pretty_json(sys.argv[3], extended_attributes)
