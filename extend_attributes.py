'''
Extend the list of DICOM attributes with the extra properties from the DICOM data
element registry in section 6.

In particular, extend the attributes with the VR, VM, keyword, and retired fields.
'''
import sys
import re

from parse_lib import write_pretty_json, read_json_to_dict

hardcoded_key_matches = {"Water Equivalent Diameter Method Code Sequence": "Water Equivalent Diameter Calculation Method Code Sequence" }

def left_join(left_list, right_dict, key):
    joined = {}
    for left_row in left_list: 
        try:
            right_row = right_dict[left_row[key]]
        except KeyError as e:
            message = "Error joining the tables on key {}. Left row {}"
            raise Exception(message.format(left_row[key], left_row))
        check_overlapping_key_similarity(left_row, right_row)
        joined[left_row[key]] = {**left_row, **right_row}
    return joined


def check_overlapping_key_similarity(left, right):
    '''
    Fuzzy compare to handle spelling and formatting differences between
    PS3.3 and PS3.6
    '''
    overlapping_keys = set(left.keys()) & set(right.keys())
    for k in overlapping_keys:
        if not fuzzy_equal(left[k], right[k]) and not hardcoded_match(left[k], right[k]):
            message = 'Error when joining by {}.  Left = "{}", right = "{}"'
            raise Exception(message.format(k, left[k], right[k]))


def hardcoded_match(left_name, right_name):
    for key, value in hardcoded_key_matches.items():
        if key == left_name and value == right_name:
            return True
    return False


def fuzzy_equal(left_name, right_name):
    left_bare = remove_all_formatting(left_name)
    right_bare = remove_all_formatting(right_name)
    return left_bare == right_bare


def remove_all_formatting(name):
    non_alphanumeric_characters = re.compile('\W')
    alphanumeric_name = non_alphanumeric_characters.sub('', name)
    return alphanumeric_name.strip().lower().replace("-","").replace(" ", "")

if __name__ == '__main__':
    modules = read_json_to_dict(sys.argv[1])
    data_element_registry = read_json_to_dict(sys.argv[2])
    extended_attributes = {}
    for module in modules:
        parsed_attribute = left_join(module['data'], data_element_registry, 'tag')
        extended_attributes = {**extended_attributes, **parsed_attribute}
    # extended_attributes = left_join(attributes, data_element_registry, 'tag')
    write_pretty_json(sys.argv[3], extended_attributes)
