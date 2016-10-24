import sys
from bs4 import BeautifulSoup

import parse_lib as pl

BASE_URL = "http://dicom.nema.org/medical/dicom/current/output/html/"

def ciod_table_from_raw_list(ciod_module_list):
    ciods = {}
    for ciod in ciod_module_list:
        ciods[ciod['id']] = {
            'id': ciod['id'],
            'description': clean_description(ciod['description']),
            'linkToStandard': ciod['linkToStandard'],
            'name': ciod['name'],
            'order': ciod['order']
        }
    return ciods

def clean_description(raw_html):
    description_html = BeautifulSoup(raw_html, 'html.parser')
    top_level_tag = description_html.find('p', recursive=False)
    if top_level_tag is None:
        top_level_tag = description_html.find('div', recursive=False)
    tag_with_no_extra_attributes = pl.remove_attributes_from_description_html(top_level_tag)
    tag_with_resolved_hrefs = pl.resolve_hrefs(tag_with_no_extra_attributes, BASE_URL)
    return str(pl.add_targets_to_anchors(tag_with_resolved_hrefs))

if __name__ == "__main__":
    ciod_module_list = pl.read_json_to_dict(sys.argv[1])
    ciods = ciod_table_from_raw_list(ciod_module_list)
    pl.write_pretty_json(sys.argv[2], ciods)
