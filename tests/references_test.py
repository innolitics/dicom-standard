'''
Unit tests to check that all links to the DICOM Standard are valid URLs
'''
import pytest
import requests

from dicom_standard import parse_lib as pl


def get_invalid_urls(url_list):
    errors = []
    for url in url_list:
        status_code = requests.get(url).status_code
        if status_code != 200:
            errors.append(url)
    return errors


@pytest.mark.skip(reason="takes too long when running other tests")
def test_valid_references():
    references_dict = pl.read_json_data('standard/references.json')
    urls = list(references_dict.keys())
    assert not get_invalid_urls(urls)


@pytest.mark.skip(reason="takes too long when running other tests")
def test_valid_standard_links():
    module_to_attributes = pl.read_json_data('standard/module_to_attributes.json')
    links = set([rel['linkToStandard'] for rel in module_to_attributes])
    assert not get_invalid_urls(links)
