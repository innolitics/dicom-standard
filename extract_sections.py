import sys
import re
from bs4 import BeautifulSoup

from parse_lib import parse_html_file, write_pretty_json

referenced_ids = r'(sect.*)|(figure.*)|(biblio.*)|(table.*)|(note.*)'
BASE_DICOM_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def extract_section_ids(standard):
    return {page: html.find_all('a', attrs={'id': re.compile(referenced_ids)})
            for page, html in standard.items()}

def section_html_from_id_anchor(sect_id_anchor):
    if re.match(r'sect.*', sect_id_anchor['id']):
        return sect_id_anchor.parent.parent.parent.parent.parent
    elif re.match(r'(biblio.*)|(table.*)|(note.*)', sect_id_anchor['id']):
        return sect_id_anchor.parent
    elif re.match(r'figure.*', sect_id_anchor['id']):
        return sect_id_anchor.parent
    else:
        print(sect_id_anchor.parent)
        raise Exception


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
