'''
Save reference HTML into a separate JSON file.
'''
import sys
import re

from bs4 import BeautifulSoup

import parse_lib as pl
from macro_utils import flatten_one_layer
from postprocess_mark_references import references_from_module_attr_pair


def find_reference_html_in_sections(pairs, section_listing):
    refs_to_record = get_refs_from_pairs(pairs)
    references = {pl.BASE_SHORT_DICOM_SECTION_URL + chapter + '/' + page_and_section:
                  section_listing[chapter + '.html'][page_and_section.split('#')[-1]]
                  for chapter, page_and_section in refs_to_record}
    refs_with_resolved_resource_urls = {k: pl.resolve_relative_resource_urls(v)
                                        for k, v in references.items()}
    cleaned_references = {k: pl.clean_html(v) for k, v in refs_with_resolved_resource_urls.items()}
    return cleaned_references

def section_parent_page(sect_div):
    parent_section_id = sect_div.parent.div.div.div.find('a').get('id')
    sections = parent_section_id.split('.')
    try:
        cutoff_index = sections.index('1')
        return '.'.join(sections[0:cutoff_index])
    except ValueError:
        return parent_section_id


def get_refs_from_pairs(pairs):
    refs_to_record = set()
    for pair in pairs:
        ref_page_id_pairs = map(get_location_from_ref, pair['externalReferences'])
        for ref in ref_page_id_pairs:
            refs_to_record.add(ref)
    return refs_to_record


def get_location_from_ref(ref):
    _, standard_location = ref['sourceUrl'].split(pl.BASE_SHORT_DICOM_SECTION_URL)
    chapter, page_and_section = standard_location.split('/')
    return chapter, page_and_section


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    section_listing = pl.read_json_to_dict(sys.argv[2])
    references = find_reference_html_in_sections(module_attr_pairs, section_listing)
    pl.write_pretty_json(references)
