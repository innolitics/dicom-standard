from bs4 import BeautifulSoup

import tests.html_snippets
import parse_lib as pl

def test_flat():
    table = BeautifulSoup(tests.html_snippets.flat, 'html.parser')
    table_list = pl.table_to_list(table)
    expected_table_list = [ ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'] ]
    assert table_list == expected_table_list 

def test_with_links():
    table = BeautifulSoup(tests.html_snippets.with_links, 'html.parser')
    table_list = pl.table_to_list(table)
    expected_table_list = [ ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'] ]
    assert table_list == expected_table_list

def test_rowspan():
    table = BeautifulSoup(tests.html_snippets.rowspan, 'html.parser')
    table_list = pl.table_to_list(table)
    expected_table_list = [ ['<td rowspan="3"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>2</td>', '<td>3</td>', '<td>4</td>', None],
                    ['<td>2</td>', '<td>3</td>', '<td>4</td>', None] ]
    assert table_list == expected_table_list

def test_colspan():
    table = BeautifulSoup(tests.html_snippets.colspan, 'html.parser')
    table_list = pl.table_to_list(table)
    expected_table_list = [ ['<td colspan="3"><a href="somelink">1</a></td>', '<td>4</td>', None, None],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'] ]
    assert table_list == expected_table_list 

def test_slide():
    row = [1., 2., None, None]
    start_idx = 0
    num_slides = 2
    row = pl.slide_down(start_idx, num_slides, row)
    expected_row = [1., 2., None, 2.]
    assert row == expected_row

def test_expand_colspan():
    table = BeautifulSoup(tests.html_snippets.colspan, 'html.parser')
    table_list = pl.table_to_list(table)
    table_list = pl.expand_spans(table_list)
    expected_table_list = [ ['<a href="somelink">1</a>', '<a href="somelink">1</a>', '<a href="somelink">1</a>', '4'],
                    ['1','2','3','4'],
                    ['1','2','3','4']]
    assert table_list == expected_table_list

def test_expand_rowspan():
    table = BeautifulSoup(tests.html_snippets.rowspan, 'html.parser')
    table_list = pl.table_to_list(table)
    table_list = pl.expand_spans(table_list)
    expected_table_list = [ ['<a href="somelink">1</a>', '2', '3', '4'],
                    ['<a href="somelink">1</a>', '2', '3', '4'],
                    ['<a href="somelink">1</a>', '2', '3', '4']]
    assert table_list == expected_table_list

def test_expand_both():
    table = BeautifulSoup(tests.html_snippets.bothspan, 'html.parser')
    table_list = pl.table_to_list(table)
    table_list = pl.expand_spans(table_list)
    expected_table_list = [ ['<a href="somelink">1</a>', '<a href="somelink">1</a>', '<a href="somelink">1</a>', '4'],
                    ['<a href="somelink">1</a>', '<a href="somelink">1</a>', '<a href="somelink">1</a>', '4'],
                    ['1','2','3','4']]
    assert table_list == expected_table_list
