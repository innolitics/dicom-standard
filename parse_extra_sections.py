import sys
import re
from bs4 import BeautifulSoup

import parse_lib as pl


def parse_extra_sections(modules_with_attributes, parseable_html):
    extra_sections = {}
    for module in modules_with_attributes:
        module_attributes = module['data']
        for attribute in module_attributes:
            referenced_sections = get_referenced_sections(attribute, parseable_html)
            extra_sections[attribute['path']] = referenced_sections
    return extra_sections

def get_referenced_sections(attribute, parseable_html):
    description_html = BeautifulSoup(attribute['description'], 'html.parser')
    top_level_tags = description_html.contents
    sections = []
    for tag in top_level_tags:
        anchors = tag.find_all('a')
        for anchor in anchors:
            if 'href' in anchor.attrs.keys():
                section_reference = anchor['href'].split('#')
                sections.append(get_section_or_fig_from_reference(section_reference[-1], parseable_html)) 
    return sections

def get_section_or_fig_from_reference(section_id, parseable_html):
    # TODO: There are two distinct reference types:
    #       1. References to sections
    #       2. References to figures (haven't implemented yet)
    # Need to regex match and treat each case separately
    id_tag = parseable_html.find(id=section_id)
    if re.match('sect', section_id):
        referenced_html = get_section_html(id_tag)
    return referenced_html

def get_section_html(id_tag):
    return id_tag.parent.parent.parent.parent.parent

if __name__ == "__main__":
    modules_with_attributes = pl.read_json_to_dict(sys.argv[2])
    parseable_html = BeautifulSoup(sys.argv[3], 'html.parser')
    extra_sections = parse_extra_sections(modules_with_attributes, parseable_html)
    pl.write_pretty_json(sys.argv[1], extra_sections)
