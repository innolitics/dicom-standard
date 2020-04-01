'''
Unit test to confirm URLs in references.json are valid
'''
import requests

from dicom_standard import parse_lib as pl


def test_valid_references():
    references_dict = pl.read_json_to_dict('standard/references.json')
    errors = []
    for url in references_dict:
        status_code = requests.get(url).status_code
        if status_code != 200:
            errors.append(url)
    assert not errors
