import sys
import re

import parse_lib as pl


def add_attribute_slugs(attributes):
    for attribute in attributes:
        attribute['id'] = pl.create_slug(attribute['tag'])


def add_attribute_parent_ids(attributes):
    previous_attribute = {}
    for attribute in attributes:
        sequence_indicator = pl.sequence_indicator_from_cell(attribute['name'])
        if previous_attribute == {}:
            attribute['parentId'] = None
        else:
            attribute['parentId'] = record_parent_id_to_attribute(sequence_indicator,
                                                                     previous_attribute,
                                                                     attributes)
            if attribute['parentId'] is not None:
                attribute['id'] = attribute['parentId'] + ":" + attribute['id']
        previous_attribute = set_new_previous_attribute(attribute)


def set_new_previous_attribute(attribute):
    sequence_indicator = pl.sequence_indicator_from_cell(attribute['name'])
    previous_attribute = {
        'id': attribute['id'],
        'sequence_indicator': sequence_indicator,
        'parentId': attribute['parentId']
    }
    return previous_attribute


def record_parent_id_to_attribute(sequence_indicator, previous_attribute, attributes):
    if is_sub_attribute_of_previous(sequence_indicator, previous_attribute):
        return previous_attribute['id']
    elif is_same_level_as_previous(sequence_indicator, previous_attribute):
        return previous_attribute['parentId']
    else:
        return find_non_adjacent_parent(sequence_indicator, previous_attribute, attributes)


def find_non_adjacent_parent(sequence_indicator, previous_attribute, attributes):
    difference = reference_level_difference(sequence_indicator, previous_attribute)
    parentId = previous_attribute['parentId']
    for i in range(difference):
        if parentId is None:
            break
        for other_attr in attributes:
            if other_attr['id'] == parentId:
                try:
                    parentId = other_attr['parentId']
                except KeyError:
                    parentId = None
                break
    return parentId


def is_sub_attribute_of_previous(sequence_indicator, previous_attribute):
    return len(sequence_indicator) > len(previous_attribute['sequence_indicator'])


def is_same_level_as_previous(sequence_indicator, previous_attribute):
    return len(sequence_indicator) == len(previous_attribute['sequence_indicator'])


def reference_level_difference(sequence_indicator, previous_attribute):
    return len(previous_attribute['sequence_indicator']) - len(sequence_indicator)

def remove_newlines_from_name(attributes):
    for attribute in attributes:
        attribute['name'] = attribute['name'].replace('\n', '')

def clean_attributes(attributes):
    for attribute in attributes:
        stripped_name = attribute['name'].replace('\n', '')
        attribute['name'] = clean_attribute_name(stripped_name)
        attribute['tag'] = attribute['tag'].upper()


def clean_attribute_name(name):
    preceding_space, *split = re.split('^(>+)', name)
    if split != []:
        return split[1].strip()
    else:
        return name


if __name__ == '__main__':
    modules_with_attributes = pl.read_json_to_dict(sys.argv[1])

    for module in modules_with_attributes:
        module_attributes = module['data']

        remove_newlines_from_name(module_attributes)
        add_attribute_slugs(module_attributes)
        add_attribute_parent_ids(module_attributes)
        clean_attributes(module_attributes)

    pl.write_pretty_json(sys.argv[2], modules_with_attributes)
