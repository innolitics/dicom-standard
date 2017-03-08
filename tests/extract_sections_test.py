from bs4 import BeautifulSoup as bs

from extract_sections import extract_section_ids

def create_mock_standard(mock_standard_str):
    return {k: bs(v, 'html.parser') for k, v in mock_standard_str.items()}

def stringify_mock_standard(mock_standard):
    return {k: [str(tag) for tag in v] for k, v in mock_standard.items()}

def test_extract_section_ids():
    mock_standard_str = {
        "different_ids": '<a id="sect_5"></a><a id="figure_1"></a><a id="table_1"></a>',
        "single_valid_id": '<a id="biblio_5"></a><a id="some_invalid_id"></a>',
        "no_valid_ids": '<a id="blah"></a><a id="some_invalid_id"></a>',
    }
    standard = create_mock_standard(mock_standard_str)
    expected_standard = {
        "different_ids": ['<a id="sect_5"></a>', '<a id="figure_1"></a>', '<a id="table_1"></a>'],
        "single_valid_id": ['<a id="biblio_5"></a>'],
        "no_valid_ids": [],
    }
    section_ids = extract_section_ids(standard)
    assert expected_standard == stringify_mock_standard(section_ids)
