import sys
import re
from functools import partial

from bs4 import BeautifulSoup, NavigableString

import parse_lib as pl


BASE_REMOTE_RESOURCE_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"


def parse_extra_standard_content(module_to_attributes, id_to_section_html):
    extra_sections = {}
    for attribute in module_to_attributes:
        referenced_sections, urls, updated_description = get_all_references(attribute['description'], id_to_section_html, extra_sections)
        attribute['description'] = updated_description
        attribute['urls'] = urls
        extra_sections = {**extra_sections, **referenced_sections}
    return extra_sections, module_to_attributes


def get_all_references(attribute_description, id_to_section_html, extra_sections):
    description_html = BeautifulSoup(attribute_description, 'html.parser')
    sections = {}
    urls = []
    record_html_from_anchor_ref = partial(get_reference_html_string, description_html, sections, urls, id_to_section_html, extra_sections)
    for anchor in description_html.find_all('a', href=True):
        record_html_from_anchor_ref(anchor)
    return sections, urls, str(description_html)


def get_reference_html_string(description_html, sections, urls, id_to_section_html, extra_sections, anchor):
    if anchor.get_text() in extra_sections.keys():
        mark_as_saved(anchor)
        return None
    section_reference = anchor['href'].split(BASE_REMOTE_RESOURCE_URL)[-1]
    html_string = html_string_from_reference(section_reference, id_to_section_html)
    if html_string:
        clean_html = clean_html_string(html_string)
        sections[section_reference] = {"html": clean_html, "sourceUrl": anchor['href']}
        urls.append({"text": anchor.get_text(), "sourceUrl": anchor['href']})
        mark_as_saved(anchor)


def clean_html_string(html_string):
    parseable_html = BeautifulSoup(html_string, 'html.parser')
    parent = parseable_html.find('div')
    if parent is None:
        parent = parseable_html.find('p')
    for tag in parent.descendants:
        tag = remove_attributes(tag)
    parent = remove_attributes(parent)
    cleaned_html_string = str(parent)
    abbreviation_tags_removed = re.sub("(<abbr>)|(</abbr>)", "", cleaned_html_string)
    return abbreviation_tags_removed


def remove_attributes(tag):
    allowed_attributes = ["class", "href", "src", "type", "data", "colspan", "rowspan"]
    if not isinstance(tag, NavigableString):
        tag.attrs = {k: v for k,v in tag.attrs.items() if k in allowed_attributes}
    return tag


def mark_as_saved(anchor):
    anchor['href'] = ''
    anchor.name = 'span'


def html_string_from_reference(target_section, id_to_section_html):
    if '#' not in target_section:
        # TODO: the only reference that this catches is an ftp link,
        # ftp://medical.nema.org/MEDICAL/Dicom/2004/printed/04_03pu3.pdf.
        # Skip this for now.
        return None
    target_file, section_id = target_section.split('#')
    # TODO: Load other HTML files that are referenced (part16.html, part06.html)
    #       and find their appropriate sections.
    if target_file == 'part03.html':
        id_tag = id_to_section_html[section_id]
        referenced_html = ''
        if id_tag is None:
            return None
        if re.match('sect.*', section_id):
            referenced_html = get_section_html(id_tag)
        elif re.match('biblio.*', section_id):
            referenced_html = get_bibliography_html(id_tag)
        elif re.match('table.*', section_id):
            referenced_html = get_table_html(id_tag)
        elif re.match('note.*', section_id):
            referenced_html = get_note_html(id_tag)
        elif re.match('figure.*', section_id):
            referenced_html = get_figure_html(id_tag)
        return referenced_html


def is_id_for_expandable_section(html_id):
    matching_ids = ['sect.*', 'figure.*', 'biblio.*', 'table.*', 'note.*', 'glossentry.*']
    for pattern in matching_ids:
        if re.match(pattern, html_id):
            return True
    return False


def expand_resource_links_to_absolute(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    anchors = html.find_all("a")
    imgs = html.find_all("img")
    equations = html.find_all("object")
    for a in anchors:
        if 'href' in a.attrs.keys():
            fragments = a['href'].split('#')
            if len(fragments) < 2 or fragments[0] != "":
                a['href'] = BASE_REMOTE_RESOURCE_URL + a['href']
            else:
                a['href'] = BASE_REMOTE_RESOURCE_URL + 'part03.html' + a['href']
    for img in imgs:
        if 'src' in img.attrs.keys():
            img['src'] = BASE_REMOTE_RESOURCE_URL + img['src']
    for equation in equations:
        if 'data' in equation.attrs.keys():
            equation['data'] = BASE_REMOTE_RESOURCE_URL + equation['data']
    return str(html)


def get_section_html(id_tag):
    return expand_resource_links_to_absolute(str(id_tag.parent.parent.parent.parent.parent))

def get_bibliography_html(id_tag):
    return expand_resource_links_to_absolute(str(id_tag.parent))

def get_table_html(id_tag):
    return expand_resource_links_to_absolute(str(id_tag.parent))

def get_note_html(id_tag):
    return expand_resource_links_to_absolute(str(id_tag.parent))

def get_figure_html(id_tag):
    top_div = id_tag.parent
    img_tag = top_div.div.div.img
    img_tag['src'] = BASE_REMOTE_RESOURCE_URL + img_tag['src']
    return str(id_tag.parent)


if __name__ == "__main__":
    module_to_attributes = pl.read_json_to_dict(sys.argv[3])

    with open(sys.argv[4], 'r') as standard_html:
        parseable_html = BeautifulSoup(standard_html, 'html.parser')

    id_to_section_html = {e['id']: e for e in parseable_html.find_all(id=True) if is_id_for_expandable_section(e['id'])}

    extra_sections, updated_module_attributes = parse_extra_standard_content(module_to_attributes, id_to_section_html)

    pl.write_pretty_json(sys.argv[1], extra_sections)
    pl.write_pretty_json(sys.argv[2], updated_module_attributes)
