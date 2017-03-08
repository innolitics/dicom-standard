'''
Find external references in attribute descriptions. When a reference is found,
add its source URL to the JSON file and record the referenced HTML in the
`references.json` file, keyed by the source URL. Remove any anchor tag attributes
on reference links that are successfully recorded.
'''
import sys

import parse_lib as pl
from macro_utils import flatten_one_layer
from references_utils import (resolve_relative_resource_urls, references_in_module_attr_pair,
                              get_source_url_from_section_id)

def add_refs_to_pairs(module_attr_pairs):
    reference_locations = [references_in_module_attr_pair(pair) for pair in module_attr_pairs]
    references_to_record = set(flatten_one_layer(reference_locations))
    return module_attr_pairs, references_to_record

def record_reference_html(refs_to_record, section_listing):
    references = {get_source_url_from_section_id((page, sect_id)):
                  resolve_relative_resource_urls(section_listing[page][sect_id])
                  for page, sect_id in refs_to_record}
    return references


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    section_listing = pl.read_json_to_dict(sys.argv[2])
    module_attr_with_refs, refs_to_record = add_refs_to_pairs(module_attr_pairs)
    references = record_reference_html(refs_to_record, section_listing)
    pl.write_pretty_json(sys.argv[3], module_attr_with_refs)
    pl.write_pretty_json(sys.argv[4], references)
