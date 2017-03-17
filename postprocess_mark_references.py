'''
Find and mark references to external sections in attribute descriptions.
Each reference is keyed by its source URL.
'''
import sys
import re

from bs4 import BeautifulSoup

import parse_lib as pl

IGNORED_REFERENCES_RE = re.compile(r'(.*ftp.*)|(.*http.*)|(.*part05.*)|(.*chapter.*)|(.*PS3.*)|(.*DCM.*)|(.*glossentry.*)')


def get_reference_requests_from_pairs(module_attr_pairs):
    return [references_from_module_attr_pair(pair) for pair in module_attr_pairs]

def references_from_module_attr_pair(pair):
    references = get_valid_reference_anchors(pair['description'])
    return list(map(get_ref_standard_location, references))

def get_valid_reference_anchors(html):
    anchor_tags = BeautifulSoup(html, 'html.parser').find_all('a', href=True)
    return [a for a in anchor_tags if not re.match(IGNORED_REFERENCES_RE, a['href'])]

def get_ref_standard_location(reference_anchor_tag):
    relative_link = reference_anchor_tag.get('href')
    standard_page, section_id = relative_link.split('#')
    standard_page = 'part03.html' if standard_page == '' else standard_page
    return standard_page, section_id

def record_references_inside_pairs(module_attr_pairs, refs_to_record):
    updated_pairs = [record_reference_in_pair(pair, refs)
                     for pair, refs in zip(module_attr_pairs, refs_to_record)]
    return updated_pairs

def record_reference_in_pair(pair, refs):
    references = get_valid_reference_anchors(pair['description'])
    reference_urls = list(map(get_reference_url_from_standard_location, refs))
    list(map(mark_as_recorded, references))
    pair['externalReferences'] = [] if len(reference_urls) < 1 else reference_urls
    return pair

def get_reference_url_from_standard_location(standard_location):
    return pl.BASE_DICOM_URL + '#'.join(standard_location)

def mark_as_recorded(anchor):
    anchor['href'] = ''
    anchor.name = 'span'


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    refs_to_record = get_reference_requests_from_pairs(module_attr_pairs)
    updated_pairs = record_references_inside_pairs(module_attr_pairs, refs_to_record)
    pl.write_pretty_json(updated_pairs)
