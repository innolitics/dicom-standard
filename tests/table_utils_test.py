'''
Unit tests covering functions in `table_utils.py`.
'''
from bs4 import BeautifulSoup as bs

import table_utils as t
import tests.html_snippets as tables

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

def test_expand_single_rowspan():
    rowspan_table = parsed_html_table(tables.rowspan)
    expanded_table = t.stringify_table(t.expand_rows(rowspan_table))
    expected_table = [
        ['<td rowspan="1"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td rowspan="1"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td rowspan="1"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
    ]
    assert expanded_table == expected_table

def test_expand_colspan():
    colspan_table = parsed_html_table(tables.colspan)
    expanded_table = t.stringify_table(t.expand_columns(colspan_table))
    expected_table = [
        ['<td colspan="1"><a href="somelink">1</a></td>', 'None', 'None', '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
        ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
    ]
    assert expanded_table == expected_table

