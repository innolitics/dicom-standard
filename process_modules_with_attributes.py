import sys
import re
from bs4 import BeautifulSoup
from bs4.element import Tag

import parse_lib as pl

BASE_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def add_attribute_slugs(attribute):
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

def remove_newlines_from_name(attribute):
    attribute['name'] = attribute['name'].replace('\n', '')

def clean_attribute(attribute):
    stripped_name = attribute['name'].replace('\n', '')
    attribute['name'] = clean_attribute_name(stripped_name)
    attribute['tag'] = attribute['tag'].upper()


def clean_attribute_name(name):
    preceding_space, *split = re.split('^(>+)', name)
    if split != []:
        return split[1].strip()
    else:
        return name

def addMacroLinks(attribute):
    if attribute['macro_table_id'] is not None:
        attribute['linkToStandard'] = pl.standard_link_from_fragment(attribute['macro_table_id'])
    else:
        attribute['linkToStandard'] = None

def clean_description_html(node):
    description_html = BeautifulSoup(node['description'], 'html.parser')
    top_level_tags = description_html.contents
    cleaned_html = ''
    for tag in top_level_tags:
        if not isinstance(tag, Tag):
            continue
        tag_with_no_extra_attributes = pl.remove_attributes_from_description_html(tag)
        tag_with_resolved_hrefs = pl.resolve_hrefs(tag_with_no_extra_attributes, BASE_URL)
        tag_with_target_anchors = pl.add_targets_to_anchors(tag_with_resolved_hrefs)
        cleaned_html += str(tag_with_target_anchors)
    node['description'] = cleaned_html


def modify_module_description_table_link(module):
    parsable_description = BeautifulSoup(module['description'], 'html.parser')
    anchor_tags = parsable_description.find_all('a')
    if (anchor_tags is not None):
        for anchor in anchor_tags:
            if (anchor.string is not None) and re.match("Table.*", anchor.string) is not None:
                anchor.name = 'span'
                anchor['href'] = ''
                anchor.string = 'This module'
                break
    module['description'] = str(parsable_description)


def process_module_description(module):
    clean_description_html(module)
    modify_module_description_table_link(module)


def process_attribute(attribute):
    remove_newlines_from_name(attribute)
    add_attribute_slugs(attribute)
    clean_attribute(attribute)
    addMacroLinks(attribute)
    clean_description_html(attribute)

if __name__ == '__main__':
    modules_with_attributes = pl.read_json_to_dict(sys.argv[1])

    for module in modules_with_attributes:
        module_attributes = module['data']
        process_module_description(module)
        for attribute in module_attributes:
            process_attribute(attribute)
        add_attribute_parent_ids(module_attributes)

    pl.write_pretty_json(sys.argv[2], modules_with_attributes)
