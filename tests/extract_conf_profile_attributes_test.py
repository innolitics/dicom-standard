'''
Unit tests covering functions in `extract_conf_profile_attributes.py`.
'''
import pytest

from dicom_standard.extract_conf_profile_attributes import extract_tag, table_to_json


@pytest.mark.parametrize('raw_tag,expected', [
    ('(0008,0050)', '(0008,0050)'),
    ('(50xx,xxxx)', '(50xx,xxxx)'),
    ('(gggg,eeee) where gggg is odd', '(gggg,eeee)'),
])
def test_extract_tag(raw_tag, expected):
    assert extract_tag(raw_tag) == expected


def test_extract_tag_passes_through_cell_without_a_tag():
    assert extract_tag('No tag here') == 'No tag here'


def test_table_to_json_derives_id_from_the_tag_alone():
    table = [
        {'name': 'Accession Number', 'tag': '(0008,0050)'},
        {'name': 'Curve Data', 'tag': '(50xx,xxxx)'},
        {'name': 'Private Attributes', 'tag': '(gggg,eeee) where gggg is odd'},
    ]
    attributes = table_to_json(table)
    assert [attr['tag'] for attr in attributes] == [
        '(0008,0050)', '(50XX,XXXX)', '(GGGG,EEEE)']
    assert [attr['id'] for attr in attributes] == [
        '00080050', '50xxxxxx', 'ggggeeee']
