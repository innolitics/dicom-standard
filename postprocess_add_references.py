'''
Find external references in attribute descriptions. When a reference is found,
add its source URL to the JSON file and record the referenced HTML in the
`references.json` file, keyed by the source URL. Remove any anchor tag attributes
on reference links that are successfully recorded.
'''
import sys
import re
from functools import partial

from bs4 import BeautifulSoup

import parse_lib as pl
from macro_utils import flatten_one_layer

IGNORED_REFERENCES_RE = re.compile(r'(.*ftp.*)|(.*http.*)|(.*part05.*)|(.*chapter.*)|(.*PS3.*)|(.*DCM.*)|(.*glossentry.*)')


# TODO: rewrite this so as to not have side effects in a list comprehension
# a function should either return a computed value from its inputs or modify
# the input, but almost never both.  In this case, having a function in a list
# comprehension is quite confusing.  A cursory look at add_refs_to_pairs makes
# one think that the first return value is unnecessary because it is not being
# modified anywhere.  It turns out it is NOT necessary, because the value is
# modified in place via a list comprehension!
def add_refs_to_pairs(module_attr_pairs):
    reference_locations = [references_in_module_attr_pair(pair) for pair in module_attr_pairs]
    references_to_record = set(flatten_one_layer(reference_locations))
    return module_attr_pairs, references_to_record


def record_reference_html(refs_to_record, section_listing):
    references = {get_source_url_from_section_id((page, sect_id)):
                  resolve_relative_resource_urls(section_listing[page][sect_id])
                  for page, sect_id in refs_to_record}
    return references


def references_in_module_attr_pair(pair):
    references = get_valid_reference_anchors(pair['description'])
    reference_locations = list(map(get_ref_standard_location, references))
    reference_urls = list(map(get_source_url_from_section_id, reference_locations))
    list(map(mark_as_recorded, references))
    pair['externalReferences'] = [] if len(reference_urls) < 1 else reference_urls
    return reference_locations


def get_valid_reference_anchors(html):
    anchor_tags = BeautifulSoup(html, 'html.parser').find_all('a', href=True)
    return [a for a in anchor_tags if not re.match(IGNORED_REFERENCES_RE, a['href'])]


def get_source_url_from_section_id(standard_location):
    return pl.BASE_DICOM_URL + '#'.join(standard_location)


def get_ref_standard_location(reference_anchor_tag):
    relative_link = reference_anchor_tag.get('href')
    standard_page, section_id = relative_link.split('#')
    standard_page = 'part03.html' if standard_page == '' else standard_page
    return standard_page, section_id


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
        anchor['href'] = pl.BASE_DICOM_URL + anchor['href']


def has_protocol_prefix(anchor):
    return re.match(r'(http)|(ftp)', anchor['href'])


def resolve_resource(url_attribute, resource):
    resource[url_attribute] = pl.BASE_DICOM_URL + resource[url_attribute]


def mark_as_recorded(anchor):
    anchor['href'] = ''
    anchor.name = 'span'


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    section_listing = pl.read_json_to_dict(sys.argv[2])
    module_attr_with_refs, refs_to_record = add_refs_to_pairs(module_attr_pairs)
    references = record_reference_html(refs_to_record, section_listing)
    pl.write_pretty_json(sys.argv[3], module_attr_with_refs)
    pl.write_pretty_json(sys.argv[4], references)
