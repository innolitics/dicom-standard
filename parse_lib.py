'''
Common functions for extracting information from the
DICOM standard HTML file.
'''

import json
import re
from bs4.element import Tag

from bs4 import BeautifulSoup

import parse_relations as pr

BASE_DICOM_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def parse_html_file(filepath):
    with open(filepath, 'r') as html_file:
        return BeautifulSoup(html_file, 'html.parser')


def write_pretty_json(filepath, data):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, sort_keys=False, indent=4, separators=(',', ':'))


def read_json_to_dict(filepath):
    with open(filepath, 'r') as json_file:
        json_string = json_file.read()
        json_dict = json.loads(json_string)
        return json_dict


def all_tdivs_in_chapter(standard, chapter_name):
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if chapter.div.div.div.h1.a.get('id') == chapter_name:
            table_divs = chapter.find_all('div', class_='table')
            return table_divs

def create_slug(title):
    first_pass = re.sub(r'[\s/]+', '-', title.lower())
    return re.sub(r'[\(\),\']+', '', first_pass)


def find_tdiv_by_id(all_tables, table_id):
    table_with_id = [table for table in all_tables if pr.table_id(table) == table_id]
    return None if table_with_id == [] else table_with_id[0]


def clean_table_name(name):
    _, _, title = re.split('\u00a0', name)
    possible_table_suffixes = r'(IOD Modules)|(Module Attributes)|(Macro Attributes)|(Module Table)'
    clean_title, *_ = re.split(possible_table_suffixes, title)
    return clean_title.strip()


def clean_description(description_html):
    parsed_html = BeautifulSoup(description_html, 'html.parser')
    top_level_tag = get_top_level_tag(parsed_html)
    tag_with_no_extra_attributes = remove_attributes_from_description_html(top_level_tag)
    tag_with_resolved_hrefs = resolve_hrefs(tag_with_no_extra_attributes)
    return str(tag_with_resolved_hrefs)

def get_top_level_tag(parsed_html):
    top_level_tag = parsed_html.find('p', recursive=False)
    if top_level_tag is None:
        top_level_tag = parsed_html.find('div', recursive=False)
    return top_level_tag


def remove_attributes_from_description_html(top_level_tag):
    top_level_tag.attrs = clean_tag_attributes(top_level_tag)
    for child in top_level_tag.descendants:
        if isinstance(child, Tag):
            child.attrs = clean_tag_attributes(child)
    return top_level_tag

def clean_tag_attributes(tag, ignored_attributes=None):
    if ignored_attributes is None:
        ignored_attributes = ['href']
    if tag.attrs != {}:
        return {a: v for a, v in tag.attrs.items() if a in ignored_attributes}
    else:
        return tag.attrs

def resolve_hrefs(tag):
    anchors = tag.find_all('a', href=True)
    list(map(resolve_anchor_href, anchors))
    return tag

def resolve_anchor_href(anchor):
    page, fragment_id = anchor['href'].split('#')
    resolved_page = 'part03.html' if page == '' else page
    anchor['href'] = BASE_DICOM_URL + resolved_page + '#' + fragment_id
    anchor['target'] = '_blank'

def text_from_html_string(html_string):
    parsed_html = BeautifulSoup(html_string, 'html.parser')
    return parsed_html.text.strip()
