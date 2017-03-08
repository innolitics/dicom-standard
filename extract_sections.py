import sys
import re
from bs4 import BeautifulSoup

from parse_lib import parse_html_file, write_pretty_json
from parse_relations import section_div_from_id, figure_div_from_id

referenced_ids = r'(sect.*)|(figure.*)|(biblio.*)|(table.*)|(note.*)'

def extract_section_ids(standard):
    return {page: html.find_all('a', attrs={'id': re.compile(referenced_ids)})
            for page, html in standard.items()}

def section_html_from_id_anchor(sect_id_anchor):
    if re.match(r'sect.*', sect_id_anchor['id']):
        return section_div_from_id(sect_id_anchor)
    elif re.match(r'(biblio.*)|(table.*)|(note.*)|(figure.*)', sect_id_anchor['id']):
        return figure_div_from_id(sect_id_anchor)
    else:
        raise Exception(sect_id_anchor.parent + "didn't match a known pattern.")


def normalize_sections(all_sections):
    return {section['id']: str(section_html_from_id_anchor(section)) for section in all_sections}

if __name__ == '__main__':
    standard = {
        'part03.html': parse_html_file(sys.argv[1]),
        'part04.html': parse_html_file(sys.argv[2]),
        'part06.html': parse_html_file(sys.argv[3]),
        'part15.html': parse_html_file(sys.argv[4]),
        'part16.html': parse_html_file(sys.argv[5]),
        'part17.html': parse_html_file(sys.argv[6]),
        'part18.html': parse_html_file(sys.argv[7]),
    }
    section_ids = extract_section_ids(standard)
    sections = {page: normalize_sections(html) for page, html in section_ids.items()}
    write_pretty_json(sys.argv[8], sections)
