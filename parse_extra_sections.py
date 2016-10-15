import sys
import re
from bs4 import BeautifulSoup, NavigableString

import parse_lib as pl

BASE_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def parse_extra_standard_content(module_to_attributes, parseable_html):
    extra_sections = {}
    for attribute in module_to_attributes:
        referenced_sections, updated_description = get_all_references(attribute['description'], parseable_html, extra_sections)
        attribute['description'] = updated_description
        extra_sections = {**extra_sections, **referenced_sections}
    return extra_sections, module_to_attributes

def get_all_references(attribute_description, parseable_html, extra_sections):
    description_html = BeautifulSoup(attribute_description, 'html.parser')
    top_level_tags = description_html.contents
    sections = {}
    for tag in top_level_tags:
        anchors = tag.find_all('a')
        for anchor in anchors:
            if 'href' in anchor.attrs.keys():
                if anchor.get_text() in extra_sections.keys():
                    mark_as_saved(anchor)
                    continue
                section_reference = anchor['href'].split(BASE_URL)
                html_string = html_string_from_reference(section_reference[-1], parseable_html)
                if (html_string):
                    clean_html = clean_html_string(html_string)
                    sections[anchor.get_text()] = {"html": clean_html, "sourceUrl": anchor['href']}
                    mark_as_saved(anchor)
    return sections, str(description_html)

def clean_html_string(html_string):
    parseable_html = BeautifulSoup(html_string, 'html.parser')
    parent_div = parseable_html.find('div')
    for tag in parent_div.descendants:
            tag = remove_attributes(tag)
    parent_div = remove_attributes(parent_div)
    return str(parent_div)

def remove_attributes(tag):
    allowed_attributes = ["class", "href", "src", "type", "data"]
    if not isinstance(tag, NavigableString):
        tag.attrs = {k: v for k,v in tag.attrs.items() if k in allowed_attributes}
    return tag

def mark_as_saved(anchor):
    anchor['href'] = ''
    anchor.name = 'span'

def html_string_from_reference(target_section, parseable_html):
    if '#' not in target_section:
        # TODO: the only reference that this catches is an ftp link,
        # ftp://medical.nema.org/MEDICAL/Dicom/2004/printed/04_03pu3.pdf.
        # Skip this for now.
        return None
    target_file, section_id = target_section.split('#')
    # TODO: Load other HTML files that are referenced (part16.html, part06.html)
    #       and find their appropriate sections.
    if target_file == 'part03.html':
        id_tag = parseable_html.find(id=section_id)
        referenced_html = ''
        if id_tag is None:
            return None
        if re.match('sect.*', section_id) is not None:
            referenced_html = expand_resource_links_to_absolute(get_section_html(id_tag))
        elif re.match('figure.*', section_id) is not None:
            referenced_html = get_figure_html(id_tag)
        return referenced_html

def expand_resource_links_to_absolute(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    anchors = html.find_all("a")
    imgs = html.find_all("img")
    equations = html.find_all("object")
    for a in anchors:
        if 'href' in a.attrs.keys():
            fragments = a['href'].split('#')
            if len(fragments) < 2 or fragments[0] != "":
                a['href'] = BASE_URL + a['href']
            else:
                a['href'] = BASE_URL + 'part03.html' + a['href']
    for img in imgs:
        if 'src' in img.attrs.keys():
            img['src'] = BASE_URL + img['src']
    for equation in equations:
        if 'data' in equation.attrs.keys():
            equation['data'] = BASE_URL + equation['data']
    return str(html)


def get_section_html(id_tag):
    return str(id_tag.parent.parent.parent.parent.parent)

def get_figure_html(id_tag):
    top_div = id_tag.parent
    img_tag = top_div.div.div.img
    img_tag['src'] = BASE_URL + img_tag['src']
    return str(id_tag.parent)

if __name__ == "__main__":
    with open(sys.argv[3], 'r') as standard_html:
        module_to_attributes = pl.read_json_to_dict(sys.argv[2])
        parseable_html = BeautifulSoup(standard_html, 'html.parser')
        extra_sections, updated_module_attributes = parse_extra_standard_content(module_to_attributes, parseable_html)
        pl.write_pretty_json(sys.argv[1], extra_sections)
        pl.write_pretty_json(sys.argv[2], updated_module_attributes)
