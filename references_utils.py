import re
from functools import partial

from bs4 import BeautifulSoup

from parse_lib import BASE_DICOM_URL

ignored_references = r'(.*ftp.*)|(.*http.*)|(.*part05.*)|(.*chapter.*)|(.*PS3.*)|(.*DCM.*)|(.*glossentry.*)'

def references_in_module_attr_pair(pair):
    references = get_valid_reference_anchors(pair['description'])
    reference_locations = list(map(get_ref_standard_location, references))
    reference_urls = list(map(get_source_url_from_section_id, reference_locations))
    list(map(mark_as_recorded, references))
    pair['externalReferences'] = [] if len(reference_urls) < 1 else reference_urls
    return reference_locations

def get_valid_reference_anchors(html):
    anchor_tags = BeautifulSoup(html, 'html.parser').find_all('a', href=True)
    return [a for a in anchor_tags if not re.match(ignored_references, a['href'])]

def get_source_url_from_section_id(standard_location):
    return BASE_DICOM_URL + '#'.join(standard_location)

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
        anchor['href'] = BASE_DICOM_URL + anchor['href']

def has_protocol_prefix(anchor):
    return re.match(r'(http)|(ftp)', anchor['href'])

def resolve_resource(url_attribute, resource):
    resource[url_attribute] = BASE_DICOM_URL + resource[url_attribute]

def mark_as_recorded(anchor):
    anchor['href'] = ''
    anchor.name = 'span'
