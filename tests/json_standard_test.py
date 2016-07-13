'''
Unit tests checking the json output from standard parsing.

These tests cover most of the functions in parse_lib.py. Functions
related to manipulating the tables (i.e. row or column span expansion)
are in the test_tables.py file.
'''

from bs4 import BeautifulSoup

import parse_lib as pl
import extract_ciods_with_modules as cm
import normalize_ciods as nc
import normalize_modules as nm
import normalize_attributes as na
import normalize_ciod_module_relationship as ncm
import normalize_module_attr_relationship as nma
import tests.standard_snippets


def test_table_to_dict():
    table = [['1', '2', '3'], ['4', '5', '6']]
    columns = ['col1', 'col2', 'col3']

    expected_dict = [
        {'col1': '1', 'col2': '2', 'col3': '3'},
        {'col1': '4', 'col2': '5', 'col3': '6'},
    ]

    assert pl.table_to_dict(table, columns) == expected_dict


def test_add_descriptions_to_dict():
    json_dict = [{}, {}, {}]
    descriptions = ["First", "Second", "Third"]
    descriptions_dict = cm.add_ciod_description_and_order(json_dict, descriptions)
    assert  descriptions_dict == [
        {
            "description": "First",
            "order": 0
        },
        {
            "description": "Second",
            "order": 1
        },
        {
            "description": "Third",
            "order": 2
        }
    ]

def test_get_text_or_href_from_html():
    '''
    Test text and href extraction. Note the dependence on the id <a></a> tag,
    which is present in every cell of the standard.
    '''
    cell = '<h3><a id="this is the id link"></a>This is a really cool <a href="link">link</a> to a website.</h3>'
    only_text = 'This is a really cool link to a website.'
    href_text = 'link'
    text = pl.text_or_href_from_cell(cell, 0, False)
    assert text == only_text
    link = pl.text_or_href_from_cell(cell, 2, True)
    assert link == href_text

def test_get_text_from_table():
    table = [['<h1>1</h1>', '<h1>2</h1>', '<h1>3</h1>', '<h1>4</h1>'],
             ['<h1>5</h1>', '<h1>6</h1>', '<h1>7</h1>', '<h1>8</h1>'],
             ['<h1>9</h1>', '<h1>10</h1>', '<h1>11</h1>', '<h1>12</h1>']]
    extract_links = False
    text_table = pl.extract_text_from_html(table, extract_links)
    expected_text_table = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12']]
    assert text_table == expected_text_table

def test_get_text_from_table_with_links():
    table = [['<h1>1</h1>', '<h1>2</h1>', '<h1><a id="some_id1"></a><a href="link1">3</a></h1>', '<h1>4</h1>'],
             ['<h1>5</h1>', '<h1>6</h1>', '<h1><a id="some_id2"></a><a href="link2">7</a></h1>', '<h1>8</h1>'],
             ['<h1>9</h1>', '<h1>10</h1>', '<h1><a id="some_id3"></a><a href="link3">11</a></h1>', '<h1>12</h1>']]
    extract_links = True
    text_table = pl.extract_text_from_html(table, extract_links)
    expected_text_table = [['1', '2', 'link1', '4'], ['5', '6', 'link2', '8'], ['9', '10', 'link3', '12']]
    assert text_table == expected_text_table

def test_extract_referenced_table_id():
    cell_html = '<td><p><span><a href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.3"></a></span></p></td>'
    html = BeautifulSoup(cell_html, 'html.parser')
    cell = html.find('td')
    table_id = pl.extract_referenced_table_id(cell)
    assert table_id == "sect_C.7.1.3"

def test_find_table_div():
    divs = BeautifulSoup(tests.standard_snippets.divlist, 'html.parser').find_all('div', class_='table')
    table2 = pl.find_table_div(divs, 'tbl2')
    assert table2.a.get('id') == 'tbl2'

def test_table_to_list_no_macros():
    '''
    Check conversion of tables to lists with no macros present.
    Note: the long, unbroken string is unfortunately required for matching
    and cannot be indented for better readability.
    '''
    section = BeautifulSoup(tests.standard_snippets.cr_iod_section, 'html.parser')
    tdiv = section.find('div', class_='table')
    table = pl.table_to_list(tdiv)
    expected_html = '''<td align="left" colspan="1" rowspan="2">\n<p>\n<a id="para_5aa8b3f7-568e-412b-9b86-87014069f3a3" shape="rect"></a>Patient</p>\n</td>'''
    print(table[0][0])
    assert table[0][0] == expected_html

def test_table_to_list_with_macros():
    original_table = BeautifulSoup(tests.standard_snippets.macro_caller, 'html.parser')
    original_tdiv = original_table.find('div', class_='table')
    macro_list = BeautifulSoup(tests.standard_snippets.macro_callee, 'html.parser')
    macro_tables = macro_list.find_all('div', class_='table')
    table = pl.table_to_list(original_tdiv, macro_tables)
    print(table)
    assert table == [['<td>Useful Information</td>', None, None, None]]

def test_row_to_list():
    cell1 = '<td>Cell 1</td>'
    cell2 = '<td>Cell 2</td>'
    cell3 = '<td>Cell 3</td>'
    cell4 = '<td>Cell 4</td>'
    row_html = '<tr>' + cell1 + cell2 + cell3 + cell4 + '</tr>'
    row = BeautifulSoup(row_html, 'html.parser')
    cells = pl.convert_row_to_list(row)
    assert [cell1, cell2, cell3, cell4] == cells

def test_get_td_html():
    cell = '<td align="left" rowspan="2" colspan="1">This is <a href="content_link">some content</a> I want.</td>'
    content = pl.td_html_content(cell)
    assert content == 'This is <a href="content_link">some content</a> I want.'

def test_get_span_from_cell():
    inner_html = 'This is <a href="content_link">a cell</a> with spans to be expanded.'
    cell = '<td align="left" rowspan="2" colspan="1">' + inner_html + '</td>'
    span = pl.span_from_cell(cell)
    assert [2, 1, inner_html] == span

def test_extract_data_element_registry():
    from extract_data_element_registry import extract_table_data, properties_to_dict
    properties_table = BeautifulSoup(tests.standard_snippets.properties_snippet, 'html.parser')
    table = properties_table.find('div', class_='table')
    data = extract_table_data(table.div.table.tbody)
    json_data = properties_to_dict(data)
    expected_data = {
        "keyword": "Length ToEnd",
        "valueRepresentation": "UL",
        "valueMultiplicity": '1',
        "name": "Length to End",
        "id": "00080001",
        "retired": True
    }
    assert expected_data == json_data['(0008,0001)']

def test_clean_ciod_name():
    name = 'Table\u00a0A.2-1.\u00a0CR Image IOD Modules'
    final_name = 'CR Image'
    clean_name = pl.clean_table_name(name)
    assert clean_name == final_name

def test_clean_module_name():
    name = 'Table\u00a0C.26-4.\u00a0Substance Administration Log Module Attributes'
    final_name = 'Substance Administration Log'
    clean_name = pl.clean_table_name(name)
    assert clean_name == final_name

def test_clean_macro_name():
    name = 'Table\u00a08.8-1a.\u00a0Basic Code Sequence Macro Attributes'
    final_name = 'Basic Code Sequence'
    clean_name = pl.clean_table_name(name)
    assert clean_name == final_name

def test_get_ciod_slug_from_name():
    name = 'CR Image'
    expected_slug = 'cr-image'
    assert pl.create_slug(name) == expected_slug

def test_get_module_slug_from_name():
    name = 'Substance Administration Log'
    expected_slug = 'substance-administration-log'
    assert pl.create_slug(name) == expected_slug

def test_get_macro_slug_from_name():
    name = 'Basic Code Sequence'
    expected_slug = 'basic-code-sequence'
    assert pl.create_slug(name) == expected_slug


def test_normalize_ciods():
    test_ciod_list = [
        {
            'id': 'ciod-1',
            'description': 'Some description of ciod 1.',
            'linkToStandard': 'http://somelink.com',
            'name': 'Ciod 1',
            'order': 0
        }
    ]
    ciods = nc.ciod_table_from_raw_list(test_ciod_list)
    matching_entry = test_ciod_list[0]
    del matching_entry['id']
    assert ciods['ciod-1'] == matching_entry


def test_normalize_modules():
    test_module_list = [
        {
            'id': 'module-1',
            'linkToStandard': 'http://somelink.com',
            'name': 'Module 1'
        }
    ]
    modules = nm.module_table_from_raw_list(test_module_list)
    matching_entry = test_module_list[0]
    del matching_entry['id']
    assert modules['module-1'] == matching_entry


# def test_normalize_attributes():
#     test_modules_with_attributes = [
#         {
#             'data': [
#                 {
#                     'id': '0001-0001',
#                     'name': 'Attribute 1',
#                     'parent_id': None,
#                     'type': None,
#                     'description': None,
#                     'tag': '(0001,0001)'
#                 }
#             ]
#         }
#     ]
#     attributes = na.extract_attributes(test_modules_with_attributes) # Right now, just adds an attribute id.
#     matching_entry = {
#         'name': 'Attribute 1',
#         'tag': '(0001,0001)',
#     }
#     assert attributes['(0001,0001)'] == matching_entry


def test_normalize_ciod_module_relationship():
    ciod_module_list = [
        {
            "id":"cr-image",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.2-1",
            "description":"\nThe Computed Radiography (CR) Image Information Object Definition specifies an image that has been created by a computed radiography imaging device.",
            "name":"CR Image",
            "data":[
                {
                    "informationEntity":"Patient",
                    "conditionalStatement":None,
                    "module":"Patient",
                    "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.1",
                    "usage":"M",
                },
            ]
        }
    ]
    relationship_table_list = ncm.ciod_module_relationship_table(ciod_module_list)
    expected_entry = {
        'ciod': 'cr-image',
        'module': 'patient',
        'usage': 'M',
        'conditionalStatement': None,
        'order': 0,
        'informationEntity': 'Patient'
    }
    assert relationship_table_list['cr-image:patient'] == expected_entry

def normalize_module_attribute_relationship():
    module_attribute_list = [
        {
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.2-1",
            "name":"Patient Relationship",
            "data":[
                {
                    "keyword":"ReferencedStudySequence",
                    "retired":False,
                    "valueRepresentation":"SQ",
                    "tag":"(0008,1110)",
                    "parentId":None,
                    "description":"Uniquely identifies the Study SOP Instances associated with the Patient SOP Instance. One or more Items shall be included in this Sequence.See Section\u00a010.6.1.",
                    "id":"0008-1110",
                    "valueMultiplicity":"1",
                    "type":None,
                    "name":"Referenced Study Sequence",
                }
            ],
            "id":"patient-relationship"
        }
    ]
    relationship_table_list = nma.module_attr_relationship_table(module_attribute_list)
    expected_entry = {
        'module': 'patient-relationship',
        'attribute': '0008-1110',
        'type': None,
        'order': 0
    }
    assert relationship_table_list[0] == expected_entry
