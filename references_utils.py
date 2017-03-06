import re
from functools import partial

from bs4 import BeautifulSoup

ignored_references = r'(.*ftp.*)|(.*http.*)|(.*part05.*)|(.*chapter.*)|(.*PS3.*)|(.*DCM.*)|(.*glossentry.*)'
BASE_DICOM_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def references_in_module_attr_pair(pair):
    references = get_valid_reference_anchors(pair['description'])
    standard_locations = list(map(get_ref_standard_location, references))
    reference_urls = list(map(get_source_url_from_section_id, standard_locations))
    list(map(mark_as_recorded, references))
    if len(reference_urls) > 0:
        pair['externalReferences'] = reference_urls
    return standard_locations

def get_valid_reference_anchors(html):
    anchor_tags = BeautifulSoup(html, 'html.parser').find_all('a', href=True)
    return list(filter((lambda a: not re.match(ignored_references, a['href'])), anchor_tags))

def get_source_url_from_section_id(standard_location):
    return BASE_DICOM_URL + '#'.join(standard_location)

def get_source_url(url_fragment):
    return BASE_DICOM_URL + url_fragment

def get_ref_standard_location(reference_anchor_tag):
    relative_link = reference_anchor_tag.get('href')
    standard_page, section_id = relative_link.split('#')
    standard_page = 'part03.html' if standard_page == '' else standard_page
    return standard_page, section_id


def resolve_relative_resource_urls(html_string):
    html = BeautifulSoup(html_string, 'html.parser')
    anchors = html.find_all('a', href=True)
    list(map(resolve_anchor_href, anchors))
    imgs = html.find_all("img", src=True)
    list(map(partial(resolve_resource, 'src'), imgs))
    equations = html.find_all("object", data=True)
    list(map(partial(resolve_resource, 'data'), equations))
    return str(html)

def resolve_anchor_href(anchor):
    if not has_protocol_prefix(anchor):
        anchor['href'] = get_source_url(anchor['href'])

def has_protocol_prefix(anchor):
    return re.match(r'(http)|(ftp)', anchor['href'])

def resolve_resource(url_attribute, resource):
    resource[url_attribute] = BASE_DICOM_URL + resource[url_attribute]

def mark_as_recorded(anchor):
    anchor['href'] = ''
    anchor.name = 'span'
