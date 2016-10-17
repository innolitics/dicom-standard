import json
import io
from collections import OrderedDict

from generate_sitemaps import site_tree, print_sitemap


def test_site_tree():
    ciod_to_modules = [
        {'ciod': 'a', 'module': 'b'},
        {'ciod': 'aa', 'module': 'b'},
    ]

    module_to_attributes = [
        {'path': 'b:c:d:e'},
        {'path': 'b:c:d:f'},
        {'path': 'b:c:g'},
    ]


    module_tree = {'c': {
        'd': {'e': {}, 'f': {}},
        'g': {},
    }}

    expected_site_tree = {
        'a': {'b': module_tree},
        'aa': {'b': module_tree},
    }

    assert site_tree(ciod_to_modules, module_to_attributes) == expected_site_tree


def test_print_sitemap():
    tree = {'c': {
        'd': {'e': {}, 'f': {}},
        'g': {},
    }}

    expected_lines_no_base_url = [
        '',
        '/c',
        '/c/d',
        '/c/d/e',
        '/c/d/f',
        '/c/g',
    ]

    base_url = 'asdf'
    fake_file = io.StringIO()
    print_sitemap(base_url, tree, fake_file)

    actual_lines = fake_file.getvalue().split('\n')[:-1]

    assert set(actual_lines) == set(base_url + l for l in expected_lines_no_base_url)
