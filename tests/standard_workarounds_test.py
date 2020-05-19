import pytest
import requests

from dicom_standard.parse_lib import NONSTANDARD_SECTION_IDS, SHORT_DICOM_URL_PREFIX, parse_html_file
from dicom_standard.table_utils import get_table_rows_from_ids


@pytest.fixture(scope='module')
def part03():
    return parse_html_file('dicom_standard/standard/part03.html')


def get_table_title_from_id(standard, table_id):
    table_id_element = standard.find('a', {'id': table_id})
    return table_id_element.find_next('p').text.strip()


def test_upper_case_S_in_table_a_39_19_1(part03):
    table_title = get_table_title_from_id(part03, 'table_A.35.19-1')
    assert table_title.endswith('S'), 'Table title no longer ends with upper case "S"'


def test_extra_s_in_table_a_32_9_2(part03):
    table_title = get_table_title_from_id(part03, 'table_A.32.9-2')
    assert 'Groups' in table_title, 'Table title no longer contains extra "s" at end of "Group"'


def test_missing_word_in_table_a_52_4_3_1(part03):
    table_title = get_table_title_from_id(part03, 'table_A.52.4.3-1')
    assert 'Image' not in table_title, 'Table title now contains full IOD name ("Ophthalmic Tomography Image")'


def test_extra_word_in_table_c_8_125(part03):
    table_title = get_table_title_from_id(part03, 'table_C.8-125')
    assert 'Sequence' in table_title, 'Table title no longer contains extra "Sequence"'


def test_extra_word_in_table_a_84_3_2_1(part03):
    rows = get_table_rows_from_ids(part03, ['table_A.84.3.2-1'], col_titles=['macro_name'])
    macro_name = 'Frame VOI LUT With LUT'
    row = next(filter(lambda r: macro_name in r['macro_name'], rows))
    assert 'Macro' in row['macro_name'], 'Row no longer contains extra "Macro"'


def test_extra_hierarchy_marker_in_table_c_8_25_16_8(part03):
    rows = get_table_rows_from_ids(part03, ['table_C.8.25.16-8'], col_titles=['attribute_name'])
    attr_name_substr = 'Include Table'
    row = next(filter(lambda r: attr_name_substr in r['attribute_name'], rows))
    assert '>>' in row['attribute_name'], 'Row no longer contains two hierarchy markers'


def test_missing_ie_field_in_table_a_32_10_1(part03):
    rows = get_table_rows_from_ids(part03, ['table_A.32.10-1'], col_titles=['information_entity', 'module'])
    empty_ie_rows = list(filter(lambda r: not r['information_entity'], rows))
    assert empty_ie_rows, 'Table no longer contains rows with empty IE field'


def test_sect_tid_1004_invalid_url():
    test_url = 'http://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_TID_1004.html#sect_TID_1004'
    status_code = requests.get(test_url).status_code
    assert status_code == 404, 'Section TID 1004 now has a URL format consistent with the other sections'


def test_nonstandard_sections_invalid_url():
    standard_sections = []
    for sect_id in NONSTANDARD_SECTION_IDS:
        test_url = f'{SHORT_DICOM_URL_PREFIX}{sect_id}.2.html'
        status_code = requests.get(test_url).status_code
        if status_code != 404:
            standard_sections.append(sect_id)
    sections_str = ', '.join(standard_sections)
    assert not standard_sections, f'Section(s) {sections_str} have at least one valid subsection URL'
