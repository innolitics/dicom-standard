from collections import defaultdict
import json

from parse_lib import create_slug, read_json_to_dict


def site_tree(ciod_to_modules, module_to_attributes):
    '''
    Build a tree representation (a nested dict) of the URL structure of the
    site.
    '''
    module_trees = defaultdict(lambda: {})
    for relationship in module_to_attributes:
        module, *path = relationship['path'].split(':')
        parent = module_trees[module]
        for segment in path:
            if segment not in parent:
                parent[segment] = {}
            parent = parent[segment]

    site_tree = defaultdict(lambda: {})
    for relationship in ciod_to_modules:
        ciod = relationship['ciod']
        module = relationship['module']
        site_tree[ciod][module] = module_trees[module]

    return site_tree


def print_sitemap_index(base_url, sitemap_names, f):
    print('<?xml version="1.0" encoding="UTF-8"?>', file=f)
    print('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', file=f)
    for sitemap_name in sitemap_names:
        sitemap_url = base_url + '/' + sitemap_name + '.sitemap.txt'
        print('<sitemap><loc>' + sitemap_url + '</loc></sitemap>', file=f)
    print('</sitemapindex>', file=f)


def print_sitemap(base_url, tree, f):
    print(base_url, file=f)
    for path_part, sub_tree in tree.items():
        print_sitemap(base_url + '/' + path_part, sub_tree, f)


if __name__ == "__main__":
    base_site_url = 'http://dicom.innolitics.com'

    ciod_to_modules = read_json_to_dict('./dist/ciod_to_modules.json')
    module_to_attributes = read_json_to_dict('./dist/module_to_attributes.json')

    site_tree = site_tree(ciod_to_modules, module_to_attributes)

    with open("./sitemap/sitemapindex.xml", "w") as sitemap_index_file:
        base_sitemap_url = base_site_url + '/sitemaps'
        ciods = site_tree.keys()
        print_sitemap_index(base_sitemap_url, ciods, sitemap_index_file)

    for ciod, module_tree in site_tree.items():
        base_url = base_site_url + '/ciods/' + ciod
        with open("./sitemap/" + ciod + ".sitemap.txt", "w") as sitemap_file:
            print_sitemap(base_url, module_tree, sitemap_file)
