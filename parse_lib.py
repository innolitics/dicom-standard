'''
Common functions for extracting information from the
DICOM standard HTML file.
'''

import json
import re
from bs4.element import Tag

from bs4 import BeautifulSoup

FULL_TABLE_COLUMN_NUM = 4
REFERENCE_COLUMN = 2

BASE_DICOM_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def all_tdivs_in_chapter(standard, chapter_name):
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if chapter.div.div.div.h1.a.get('id') == chapter_name:
            table_divs = chapter.find_all('div', class_='table')
            return table_divs

def create_slug(title):
    first_pass = re.sub(r'[\s/]+', '-', title.lower())
    return re.sub(r'[\(\),\']+', '', first_pass)


def find_spans(table):
    '''
    Find all rowspans and colspans in an HTML table. Returns a 2D list of
    tuples of the form (rowspan value, colspan value, html content)
    '''
    spans = []
    for row in table:
        row_spans = []
        for column, cell in enumerate(row):
            description_cell = column == 3
            cell_span = span_from_cell(cell, description_cell)
            row_spans.append(cell_span)
        spans.append(row_spans)
    return spans


def span_from_cell(cell, description_cell):
    if cell is None:
        return None
    cell_html = BeautifulSoup(cell, 'html.parser')
    td_tag = cell_html.find('td')
    try:
        if description_cell:
            return [
                int(td_tag.get('rowspan', 1)),
                int(td_tag.get('colspan', 1)),
                get_raw_inner_html(td_tag)
            ]
        else:
            return [
                int(td_tag.get('rowspan', 1)),
                int(td_tag.get('colspan', 1)),
                td_html_content(str(td_tag))
            ]
    except AttributeError:
        return [1, 1, cell]

def get_raw_inner_html(tag):
    return ''.join(list(map(str, tag.contents)))

def td_html_content(td_html):
    split_html = re.split('(<td.*?>)|(</td>)', td_html)
    return split_html[3]


def find_table_div(all_tables, table_id):
    try:
        for table in all_tables:
            if table.a.get('id') == table_id:
                return table
        return None
    except AttributeError:
        return None


def clean_table_name(name):
    _, _, title = re.split('\u00a0', name)
    clean_title, *_ = re.split(r'(IOD Modules)|(Module Attributes)|(Macro Attributes)|(Module Table)', title)
    return clean_title.strip()


def clean_description(description_html):
    parsed_html = BeautifulSoup(description_html, 'html.parser')
    top_level_tag = get_top_level_tag(parsed_html)
    tag_with_no_extra_attributes = remove_attributes_from_description_html(top_level_tag)
    tag_with_resolved_hrefs = resolve_hrefs(tag_with_no_extra_attributes, BASE_DICOM_URL)
    return str(add_targets_to_anchors(tag_with_resolved_hrefs))

def get_top_level_tag(parsed_html):
    top_level_tag = parsed_html.find('p', recursive=False)
    if top_level_tag is None:
        top_level_tag = parsed_html.find('div', recursive=False)
    return top_level_tag


def standard_link_from_fragment(fragment):
    url_prefix = "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#"
    return url_prefix + fragment


def parse_html_file(filepath):
    with open(filepath, 'r') as html_file:
        return BeautifulSoup(html_file, 'html.parser')


def write_pretty_json(filepath, data, prefix=None):
    with open(filepath, 'w') as json_file:
        if prefix is not None:
            json_file.write(prefix)
        json.dump(data, json_file, sort_keys=False, indent=4, separators=(',', ':'))


def read_json_to_dict(filepath):
    with open(filepath, 'r') as json_file:
        json_string = json_file.read()
        json_dict = json.loads(json_string)
        return json_dict


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


def resolve_hrefs(tag, base_url):
    anchors = tag.find_all('a')
    for anchor in anchors:
        if 'href' in anchor.attrs.keys():
            anchor_href_split = anchor['href'].split('#')
            if anchor_href_split[0] == '':
                anchor['href'] = base_url + 'part03.html'+ anchor['href']
            else:
                anchor['href'] = base_url + anchor['href']
    return tag


def add_targets_to_anchors(tag):
    anchors = tag.find_all('a')
    for anchor in anchors:
        if 'href' in anchor.attrs.keys():
            anchor['target'] = '_blank'
    return tag


def text_from_html_string(html_string):
    parsed_html = BeautifulSoup(html_string, 'html.parser')
    return parsed_html.text.strip()
