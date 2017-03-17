'''
Find external references in attribute descriptions. When a reference is found,
add its source URL to the JSON file and record the referenced HTML in the
`references.json` file, keyed by the source URL. Remove any anchor tag
attributes on reference links that are successfully recorded.
'''
import sys
import re
from functools import partial

from bs4 import BeautifulSoup

import parse_lib as pl
from macro_utils import flatten_one_layer

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


def find_reference_html_in_sections(refs_from_pairs, section_listing):
    refs_to_record = set(flatten_one_layer(refs_from_pairs))
    references = {get_reference_url_from_standard_location((page, sect_id)):
                  section_listing[page][sect_id]
                  for page, sect_id in refs_to_record}
    refs_with_resolved_resource_urls = {k: resolve_relative_resource_urls(v)
                                        for k, v in references.items()}
    cleaned_references = {k: pl.clean_html(v) for k, v in refs_with_resolved_resource_urls.items()}
    return cleaned_references

def resolve_relative_resource_urls(html_string):
    html = BeautifulSoup(html_string, 'html.parser')
    anchors = html.find_all('a', href=True)
    imgs = html.find_all("img", src=True)
    equations = html.find_all("object", data=True)
    list(map(resolve_anchor_href, anchors))
    list(map(partial(resolve_resource, 'src'), imgs))
    list(map(partial(resolve_resource, 'data'), equations))
    return str(html)

def resolve_anchor_href(anchor):
    if not has_protocol_prefix(anchor):
        try:
            page, fragment_id = anchor['href'].split('#')
            resolved_page = 'part03.html' if page == '' else page
            anchor['href'] = resolved_page + '#' + fragment_id
        except ValueError:
            pass
        anchor['href'] = pl.BASE_DICOM_URL + anchor['href']


def has_protocol_prefix(anchor):
    return re.match(r'(http)|(ftp)', anchor['href'])


def resolve_resource(url_attribute, resource):
    resource[url_attribute] = pl.BASE_DICOM_URL + resource[url_attribute]


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
    section_listing = pl.read_json_to_dict(sys.argv[2])
    refs_to_record = get_reference_requests_from_pairs(module_attr_pairs)
    references = find_reference_html_in_sections(refs_to_record, section_listing)
    updated_pairs = record_references_inside_pairs(module_attr_pairs, refs_to_record)
    pl.write_pretty_json(sys.argv[3], updated_pairs)
    pl.write_pretty_json(sys.argv[4], references)
