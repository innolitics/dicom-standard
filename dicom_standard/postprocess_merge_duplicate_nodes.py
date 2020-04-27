'''
Merge nodes that have identical paths by adding conditional statments to the attribute descriptions.
'''
import re
import sys
from collections import Counter

from bs4 import BeautifulSoup

from dicom_standard import parse_lib as pl

DUPLICATE_PATH_EXCEPTIONS = ['rt-segment-annotation:00700084']


def get_description_text(raw_description):
    description = BeautifulSoup(raw_description, "html.parser")
    return description.getText()


def add_conditional_to_description(node):
    conditional = node.get('conditional')
    assert conditional is not None, f'Duplicate attribute (path: {node["path"]}) has no conditional statement.'
    conditional = re.sub(r'\.$', ':', conditional)
    formatted_conditional = f'<p style="font-weight: bold">{conditional[0].upper()}{conditional[1:]}</p>'
    node['description'] = formatted_conditional + node['description']


def merge_duplicate_nodes(module_attr_list):
    path_list = [d['path'] for d in module_attr_list]
    duplicate_paths = [k for k, v in Counter(path_list).items() if v > 1]
    path_to_node = {}
    for node in module_attr_list:
        path = node['path']
        # Standard workaround: Catch inconsistency in Table C.36.8-1 where "Content Creator's Name" attribute
        # appears twice in same hierarchy without a conditional
        # http://dicom.nema.org/medical/dicom/2019c/output/chtml/part03/sect_C.36.8.html
        if path not in DUPLICATE_PATH_EXCEPTIONS:
            if path in path_to_node:
                # Add conditional to description only if the duplicates do not have identical descriptions
                instances = filter(lambda n: n['path'] == path, module_attr_list)
                descriptions = map(lambda n: get_description_text(n['description']), instances)
                if len(set(descriptions)) > 1:
                    add_conditional_to_description(node)
                    path_to_node[path]['description'] += node['description']
                    path_to_node[path]['externalReferences'].extend(node['externalReferences'])
            else:
                if path in duplicate_paths:
                    # Add conditional to description only if the duplicates do not have identical descriptions
                    instances = filter(lambda n: n['path'] == path, module_attr_list)
                    descriptions = map(lambda n: get_description_text(n['description']), instances)
                    if len(set(descriptions)) > 1:
                        add_conditional_to_description(node)
                path_to_node[path] = node
            path_to_node[path].pop('conditional', None)
    return list(path_to_node.values())


if __name__ == "__main__":
    module_attr_list = pl.read_json_data(sys.argv[1])
    processed_module_attr_list = merge_duplicate_nodes(module_attr_list)
    pl.write_pretty_json(processed_module_attr_list)
