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
    references = {pl.BASE_DICOM_URL + '#'.join((page, sect_id)):
                  section_listing[page][sect_id]
                  for page, sect_id in refs_to_record}
    refs_with_resolved_resource_urls = {k: pl.resolve_relative_resource_urls(v)
                                        for k, v in references.items()}
    cleaned_references = {k: pl.clean_html(v) for k, v in refs_with_resolved_resource_urls.items()}
    return cleaned_references


def get_refs_from_pairs(pairs):
    refs_to_record = set()
    for pair in pairs:
        ref_page_id_pairs = map(get_page_and_id_from_ref, pair['externalReferences'])
        for ref in ref_page_id_pairs:
            refs_to_record.add(ref)
    return refs_to_record


def get_page_and_id_from_ref(ref):
    _, standard_location = ref['sourceUrl'].split(pl.BASE_DICOM_URL)
    page, sect_id = standard_location.split('#')
    return page, sect_id


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    section_listing = pl.read_json_to_dict(sys.argv[2])
    references = find_reference_html_in_sections(module_attr_pairs, section_listing)
    pl.write_pretty_json(references)
