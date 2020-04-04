'''
Common functions for extracting information from the
DICOM standard HTML file.
'''

from typing import List, Any, Union
import json
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

from dicom_standard import parse_relations as pr
from dicom_standard.macro_utils import MetadataTableType

ALLOWED_ATTRIBUTES = ["href", "src", "type", "data", "colspan", "rowspan"]
BASE_DICOM_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"
BASE_SHORT_DICOM_SECTION_URL = "http://dicom.nema.org/medical/dicom/current/output/chtml/"
NONSTANDARD_SECTION_IDS = [
    'sect_10.32',
    'sect_C.7.6.16.2',
    'sect_C.8.27.4',
    'sect_C.8.8.2.6',
    'sect_C.8.8.3.4',
    'sect_C.8.8.15.16',
    'sect_C.8.8.25.6',
    'sect_C.8.13.5.14',
    'sect_C.8.19.6.9',
    'sect_C.8.27.6.3',
]
ID_PATTERN = re.compile(r'\b(' + '|'.join(NONSTANDARD_SECTION_IDS) + r').+\b')
SHORT_DICOM_URL_PREFIX = "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/"

JsonDataType = Union[List[MetadataTableType], MetadataTableType]


def parse_html_file(filepath: str) -> BeautifulSoup:
    with open(filepath, 'r') as html_file:
        return BeautifulSoup(html_file, 'html.parser')


def write_pretty_json(data: Any) -> None:
    json.dump(data, sys.stdout, sort_keys=False, indent=4, separators=(',', ':'))


def read_json_data(filepath: str) -> JsonDataType:
    with open(filepath, 'r') as json_file:
        json_string = json_file.read()
        json_dict = json.loads(json_string)
        return json_dict


def all_tdivs_in_chapter(standard: BeautifulSoup, chapter_name: str) -> List[Tag]:
    '''
    Find all HTML tables in a given chapter of the DICOM Standard.
    '''
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if chapter.div.div.div.h1.a.get('id') == chapter_name:
            table_divs = chapter.find_all('div', class_='table')
            return table_divs
    return None


def create_slug(title: str) -> str:
    first_pass = re.sub(r'[\s/]+', '-', title.lower())
    return re.sub(r'[\(\),\']+', '', first_pass)


def find_tdiv_by_id(all_tables: List[Tag], table_id: str) -> Tag:
    '''
    Find a given table tag by its HTML ID
    '''
    matching_table = (lambda table: pr.table_id(table) == table_id)
    table_with_id = list(filter(matching_table, all_tables))
    return None if table_with_id == [] else table_with_id[0]


def clean_table_name(name: str) -> str:
    '''
    Remove table name prefixes and suffixes.

    Example:
        Table C.7-5b. Clinical Trial Series Module Attributes --> Clinical Trial Series
    '''
    _, _, title = re.split('\u00a0', name)
    # Include upper case "S" at end of "IOD Modules" to catch typo in Table A.39.19-1
    # http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.35.19.3.html
    # Include optional "s" at end of "Functional Group" to catch Table A.32.9-2
    # http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.32.9.3.4.html#table_A.32.9-2
    possible_table_suffixes = r'(IOD Module[Ss])|(Module Attributes)|((Functional Group)? Macro Attributes)|(Module Table)|(Functional Groups? Macros)'
    clean_title = re.split(possible_table_suffixes, title)[0]
    # Remove extra "Table" from table title (should be "CT Performed Procedure Protocol", not "Table CT Performed ...")
    # http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.82.html#table_A.82.1.3-1
    if clean_title.strip() == 'Table CT Performed Procedure Protocol':
        clean_title = 'CT Performed Procedure Protocol'
    # Remove extra "Sequence" from table title (should be "CT X-Ray Details", not "CT X-Ray Details Sequence")
    # http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.8.15.3.9.html#table_C.8-125
    if clean_title == 'CT X-Ray Details Sequence':
        clean_title = 'CT X-Ray Details'
    return clean_title.strip()


def clean_html(html: str) -> str:
    '''
    Removes unused attributes and empty tags from
    the HTML. Also updates relative resource URLs
    to absolute URLs.
    '''
    parsed_html = BeautifulSoup(html, 'html.parser')
    top_level_tag = get_top_level_tag(parsed_html)
    if isinstance(top_level_tag, NavigableString):
        return str(top_level_tag)
    else:
        remove_attributes_from_html_tags(top_level_tag)
        remove_empty_children(top_level_tag)
        return resolve_relative_resource_urls(str(top_level_tag))


def get_top_level_tag(parsed_html: BeautifulSoup) -> Tag:
    return next(parsed_html.descendants)


def remove_attributes_from_html_tags(top_level_tag: Tag) -> None:
    clean_tag_attributes(top_level_tag)
    for child in top_level_tag.descendants:
        clean_tag_attributes(child)


def clean_tag_attributes(tag: Tag) -> None:
    if not isinstance(tag, NavigableString):
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in ALLOWED_ATTRIBUTES}


def remove_empty_children(top_level_tag: Tag) -> None:
    empty_anchor_tags = filter((lambda a: a.text == ''), top_level_tag.find_all('a'))
    for anchor in empty_anchor_tags:
        anchor.decompose()


def resolve_relative_resource_urls(html_string: str) -> str:
    html = BeautifulSoup(html_string, 'html.parser')
    anchors = html.find_all('a', href=True)
    for a in anchors:
        update_anchor_href(a)
    imgs = html.find_all("img", src=True)
    svg_objects = html.find_all("object", data=True, type="image/svg+xml")
    svgs_as_imgs = [convert_svg_obj_to_img(html, s) for s in svg_objects]
    for obj, img in zip(svg_objects, svgs_as_imgs):
        obj.replaceWith(img)
    imgs.extend(svgs_as_imgs)
    for img in imgs:
        resolve_img_src(img)
    return str(html)


def update_anchor_href(anchor: Tag) -> None:
    if not has_protocol_prefix(anchor, 'href'):
        anchor['href'] = resolve_href_url(anchor['href'])
        anchor['target'] = '_blank'


def convert_svg_obj_to_img(html: BeautifulSoup, svg: Tag):
    '''
    Since the DICOM standard represents SVG images as `object` tags,
    they can be converted to standard `img` tags by copying the object
    `data` field into `src`. This removes some complex SVG metadata HTML
    included by the standard.
    '''
    img_tag = html.new_tag('img', src=svg['data'])
    return img_tag


def has_protocol_prefix(resource: Tag, url_attribute: str) -> bool:
    return bool(re.match(r'(http)|(ftp)', resource[url_attribute]))


def resolve_href_url(href: str) -> str:
    if re.match(r'(.*sect_.*)|(.*chapter.*)', href):
        return BASE_SHORT_DICOM_SECTION_URL + get_short_html_location(href)
    else:
        return BASE_DICOM_URL + get_long_html_location(href)


def get_short_html_location(reference_link: str) -> str:
    '''
    For a given relative URL, generate the link to the short HTML version
    of the DICOM standard.
    '''
    standard_page, section_id = reference_link.split('#')
    chapter_with_extension = 'part03.html' if standard_page == '' else standard_page
    chapter, _ = chapter_with_extension.split('.html')
    return chapter + '/' + get_standard_page(section_id) + '.html#' + section_id


def get_standard_page(sect_id: str) -> str:
    '''
    Returns the short HTML page name of the DICOM standard containing `sect_id`.
    '''
    try:
        # TODO: Remove if block (and constant) once URL once links for subsections exist (Issue #10 and related sections)
        invalid_sect_id_match = re.match(ID_PATTERN, sect_id)
        if invalid_sect_id_match:
            # For some reason, certain subsections are located within the base section, so return only the valid part
            # Ex: C.7.16.2.5.1 should be within C.7.16.2.5, but "sect_C.7.16.2.5.html" is invalid
            return invalid_sect_id_match.group(1)
        # Fix broken link produced by inconsistent URL pattern: http://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_A.html#sect_TID_1004
        if sect_id == 'sect_TID_1004':
            return 'chapter_A'
        sections = sect_id.split('.')
        cutoff_index = sections.index('1')
        cropped_section = sections[0:cutoff_index]
        section_page = '.'.join(sections[0:cutoff_index])
        if len(cropped_section) == 1:
            section_page = section_page.replace('sect_', 'chapter_')
        return section_page
    except ValueError:
        return sect_id


def get_long_html_location(reference_link: str) -> str:
    standard_page, section_id = reference_link.split('#')
    chapter_with_extension = 'part03.html' if standard_page == '' else standard_page
    return chapter_with_extension + '#' + section_id


def resolve_img_src(resource: Tag) -> None:
    if not has_protocol_prefix(resource, 'src'):
        resource['src'] = BASE_DICOM_URL + resource['src']


def text_from_html_string(html_string: str) -> str:
    parsed_html = BeautifulSoup(html_string, 'html.parser')
    return parsed_html.text.strip()


def table_parent_page(table_div: Tag) -> str:
    '''
    Return the short HTML  page name of the DICOM standard containing
    the specified `table_div`.
    '''
    parent_section_id = table_div.parent.div.div.div.find('a').get('id')
    sections = parent_section_id.split('.')
    try:
        cutoff_index = sections.index('1')
        return '.'.join(sections[0:cutoff_index])
    except ValueError:
        return parent_section_id
