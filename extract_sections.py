import sys
from bs4 import BeautifulSoup

from parse_lib import parse_html_file, write_pretty_json

def get_section_id(section):
    return section.div.div.div.find('a')['id']

def normalize_sections(all_sections):
    normalized_sections = {}
    for section in raw_sections:
        normalized_sections[get_section_id(section)] = str(section)
    return normalized_sections

if __name__ == '__main__':
    standard = parse_html_file(sys.argv[1])
    raw_sections = standard.find_all('div', class_='section')
    sections = normalize_sections(raw_sections)
    write_pretty_json(sys.argv[2], sections)
