'''
Find and mark references to external sections in attribute descriptions.
Each reference is keyed by its source URL.
'''
import sys
import re

from bs4 import BeautifulSoup

from dicom_standard import parse_lib as pl

IGNORED_REFS_RE = re.compile(r'(.*ftp.*)|(.*http.*)|(.*part05.*)|(.*chapter.*)|(.*PS3.*)|(.*DCM.*)|(.*glossentry.*)')


def get_valid_reference_anchors(parsed_html):
    anchor_tags = parsed_html.find_all('a', href=True)
    return [a for a in anchor_tags if not re.match(IGNORED_REFS_RE, a['href'])]


def record_references_inside_pairs(module_attr_pairs):
    updated_pairs = [record_reference_in_pair(pair) for pair in module_attr_pairs]
    return updated_pairs


def record_reference_in_pair(pair):
    parsed_description = BeautifulSoup(pair['description'], 'html.parser')
    references = get_valid_reference_anchors(parsed_description)
    external_references = list(map(reference_structure_from_anchor, references))
    for ref in references:
        mark_as_recorded(ref)
    pair['externalReferences'] = [] if len(external_references) < 1 else external_references
    pair['description'] = str(parsed_description)
    finalize_descriptions(pair)
    return pair


def finalize_descriptions(pair):
    pair['description'] = pl.clean_html(pair['description'])


def reference_structure_from_anchor(reference):
    return {
        "sourceUrl": reference.get('href'),
        "title": reference.get_text()
    }


def mark_as_recorded(anchor):
    anchor['href'] = ''
    anchor.name = 'span'


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_data(sys.argv[1])
    updated_pairs = record_references_inside_pairs(module_attr_pairs)
    pl.write_pretty_json(updated_pairs)
