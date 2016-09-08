import sys
import re
from bs4 import BeautifulSoup

import parse_lib as pl

BASE_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def parse_extra_standard_content(module_to_attributes, parseable_html):
    extra_sections = {}
    for attribute in module_to_attributes:
        referenced_sections = get_all_references(attribute, parseable_html, extra_sections)
        extra_sections = {**extra_sections, **referenced_sections}
    return extra_sections

def get_all_references(attribute, parseable_html, extra_sections):
    description_html = BeautifulSoup(attribute['description'], 'html.parser')
    top_level_tags = description_html.contents
    sections = {}
    for tag in top_level_tags:
        anchors = tag.find_all('a')
        for anchor in anchors:
            if 'href' in anchor.attrs.keys():
                if anchor.get_text() in extra_sections.keys():
                    continue
                section_reference = anchor['href'].split(BASE_URL)
                sections[anchor.get_text()] = html_string_from_reference(section_reference[-1], parseable_html)
    return sections

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
            referenced_html = get_section_html(id_tag)
        elif re.match('figure.*', section_id) is not None:
            referenced_html = get_figure_html(id_tag)
        return referenced_html

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
        extra_sections = parse_extra_standard_content(module_to_attributes, parseable_html)
        pl.write_pretty_json(sys.argv[1], extra_sections)
