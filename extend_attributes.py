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
        except KeyError as e:
            message = "Error joining the tables on key {}. Left row {}"
            raise Exception(message.format(key, left_row))

        check_overlapping_key_similarity(left_row, right_row)
        joined[key] = {**left_row, **right_row}
    return joined


def check_overlapping_key_similarity(left, right):
    overlapping_keys = set(left.keys()) & set(right.keys())
    for k in overlapping_keys:
        assert left[k] == right[k]


if __name__ == '__main__':
    attributes = read_json_to_dict(sys.argv[1])
    data_element_registry = read_json_to_dict(sys.argv[2])
    extended_attributes = left_join(attributes, data_element_registry, 'tag')
    write_pretty_json(sys.argv[3], extended_attributes)
