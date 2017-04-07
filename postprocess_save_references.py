'''
Save reference HTML into a separate JSON file.
'''
import sys
import re

from bs4 import BeautifulSoup

import parse_lib as pl
from macro_utils import flatten_one_layer


def find_reference_html_in_sections(pairs, section_listing):
    refs_to_record = get_refs_from_pairs(pairs)
    references = {}
    for chapter, page_and_fragment in refs_to_record:
        reference_id = page_and_fragment.split('#')[-1]
        section_with_context = BeautifulSoup(section_listing[chapter + '.html'][reference_id], 'html.parser')
        enclosing_section = section_with_context.find('div').find('a', id=True)['id']
        short_dicom_url = (pl.BASE_SHORT_DICOM_SECTION_URL + chapter + '/' +
                           get_standard_page(enclosing_section) + '.html#' + reference_id)
        reference_html = section_with_context.find('a', id=reference_id)
        references[short_dicom_url] = str(reference_content_from_id(reference_html))
    refs_with_resolved_resource_urls = {k: pl.resolve_relative_resource_urls(v)
                                        for k, v in references.items()}
    cleaned_references = {k: pl.clean_html(v) for k, v in refs_with_resolved_resource_urls.items()}
    return cleaned_references


def reference_content_from_id(ref_id):
    if re.match(r'sect.*', ref_id['id']):
        return ref_id.parent.parent.parent.parent.parent
    else:
        return ref_id.parent


def section_parent_page(sect_div):
    parent_section_id = sect_div.parent.div.div.div.find('a').get('id')
    sections = parent_section_id.split('.')
    try:
        cutoff_index = sections.index('1')
        return '.'.join(sections[0:cutoff_index])
    except ValueError:
        return parent_section_id


def get_resolved_reference_href(reference_link):
    standard_page, section_id = reference_link.split('#')
    chapter_with_extension = 'part03.html' if standard_page == '' else standard_page
    chapter, _ = chapter_with_extension.split('.html')
    return chapter + '/' + get_standard_page(section_id) + '.html#' + section_id


def get_standard_page(sect_id):
    sections = sect_id.split('.')
    try:
        cutoff_index = sections.index('1')
        return '.'.join(sections[0:cutoff_index])
    except ValueError:
        return sect_id


def get_refs_from_pairs(pairs):
    refs_to_record = set()
    for pair in pairs:
        ref_page_id_pairs = map(get_location_from_ref, pair['externalReferences'])
        for ref in ref_page_id_pairs:
            refs_to_record.add(ref)
    return refs_to_record


def get_location_from_ref(ref):
    return tuple(get_resolved_reference_href(ref['sourceUrl']).split('/'))


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    section_listing = pl.read_json_to_dict(sys.argv[2])
    references = find_reference_html_in_sections(module_attr_pairs, section_listing)
    pl.write_pretty_json(references)
