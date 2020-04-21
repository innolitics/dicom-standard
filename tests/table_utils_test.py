'''
Unit tests covering functions in `table_utils.py`.
'''
from bs4 import BeautifulSoup as bs

import dicom_standard.table_utils as t
import tests.html_snippets as tables


def test_table_to_list():
    example_table = '''
    <tbody>
        <tr><td>Data</td><td>inside</td><td>this</td><td>table</td></tr>
        <tr><td>should</td><td>be</td><td>a</td><td>list</td></tr>
    </tbody
    '''
    table = bs(example_table, 'html.parser')
    expected_table_list = [['Data', 'inside', 'this', 'table'],
                           ['should', 'be', 'a', 'list']]
    table_as_list_of_lists = t.table_to_list(table)
    assert expected_table_list == table_as_list_of_lists


def parsed_html_table(string_table):
    parsed_html = bs(string_table, 'html.parser')
    table_tag = parsed_html.find('tbody')
    all_rows = table_tag.find_all('tr')
    parsed_table = [list(row.find_all('td')) for row in all_rows]
    return parsed_table


def test_slide_at_start():
    row = [1., 2.]
    start_idx = 0
    num_slides = 2
    row = t.slide_down(start_idx, row, num_slides)
    expected_row = [None, None, 1., 2.]
    assert row == expected_row


def test_slide_mid_row():
    row = [1., 2., 3.]
    start_idx = 1
    num_slides = 3
    row = t.slide_down(start_idx, row, num_slides)
    expected_row = [1., None, None, None, 2., 3.]
    assert row == expected_row


def test_tdiv_to_list_simple():
    table = bs(tables.flat, 'html.parser')
    table_list = t.tdiv_to_table_list(table)
    expected_table_list = [
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>']
    ]
    assert t.stringify_table(table_list) == expected_table_list


def test_tdiv_to_list_with_cell_content():
    table = bs(tables.with_links, 'html.parser')
    table_list = t.tdiv_to_table_list(table)
    expected_table_list = [
        ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>']
    ]
    assert t.stringify_table(table_list) == expected_table_list


def test_expand_rowspan():
    rowspan_table = parsed_html_table(tables.rowspan)
    expanded_table = t.stringify_table(t.expand_spans(rowspan_table))
    expected_table = [
        ['<td rowspan="1"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td rowspan="1"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td rowspan="1"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
    ]
    assert expanded_table == expected_table


def test_expand_colspan():
    colspan_table = parsed_html_table(tables.colspan)
    expanded_table = t.stringify_table(t.expand_spans(colspan_table))
    expected_table = [
        ['<td colspan="1"><a href="somelink">1</a></td>', 'None', 'None', '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td colspan="1"><a href="somelink">1</a></td>', 'None', 'None', '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
    ]
    assert expanded_table == expected_table


def test_expand_both():
    table = bs(tables.bothspan, 'html.parser')
    table_list = t.expand_spans(t.tdiv_to_table_list(table))
    expected_table_list = [
        ['<td colspan="1" rowspan="1"><a href="somelink">1</a></td>',
         'None',
         'None',
         '<td>4</td>'],
        ['<td colspan="1" rowspan="1"><a href="somelink">1</a></td>',
         'None',
         'None',
         '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>']
    ]
    assert t.stringify_table(table_list) == expected_table_list
