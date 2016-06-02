from bs4 import BeautifulSoup
import pandas as pd

from html_snippets import *
import parse_lib as pl

def test_flat():
    table = BeautifulSoup(flat, 'html.parser')
    df = pl.table_to_list(table)
    expected_df = [ ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'] ]
    assert df == expected_df 

def test_with_links():
    table = BeautifulSoup(with_links, 'html.parser')
    df = pl.table_to_list(table)
    expected_df = [ ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'] ]
    assert df == expected_df

def test_rowspan():
    table = BeautifulSoup(rowspan, 'html.parser')
    df = pl.table_to_list(table)
    expected_df = [ ['<td rowspan="3"><a href="somelink">1</a></td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>2</td>', '<td>3</td>', '<td>4</td>', None],
                    ['<td>2</td>', '<td>3</td>', '<td>4</td>', None] ]
    assert df == expected_df

def test_colspan():
    table = BeautifulSoup(colspan, 'html.parser')
    df = pl.table_to_list(table)
    expected_df = [ ['<td colspan="3"><a href="somelink">1</a></td>', '<td>4</td>', None, None],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'],
                    ['<td>1</td>', '<td>2</td>', '<td>3</td>', '<td>4</td>'] ]
    assert df == expected_df 

def test_slide():
    row = [1., 2., None, None]
    start_idx = 0
    num_slides = 2
    row = pl.slide_down(start_idx, num_slides, row)
    expected_row = [1., 2., None, 2.]
    assert row == expected_row

def test_get_td_html():
    tag = '<td align="left" rowspan="2" colspan="1">This is <a href="content_link">some content</a> I want.</td>'
    content = pl.get_td_html_content(tag)
    assert content == 'This is <a href="content_link">some content</a> I want.'

def test_expand_colspan():
    table = BeautifulSoup(colspan, 'html.parser')
    df = pl.table_to_list(table)
    df = pl.expand_colspan(df)
    expected_df = [ ['<a href="somelink">1</a>', '<a href="somelink">1</a>', '<a href="somelink">1</a>', '4'],
                    ['1','2','3','4'],
                    ['1','2','3','4']]
    assert df == expected_df

def test_expand_rowspan():
    table = BeautifulSoup(rowspan, 'html.parser')
    df = pl.table_to_list(table)
    print(df)
    df = pl.expand_rowspan(df)
    expected_df = [ ['<a href="somelink">1</a>', '2', '3', '4'],
                    ['<a href="somelink">1</a>', '2', '3', '4'],
                    ['<a href="somelink">1</a>', '2', '3', '4']]
    assert df == expected_df
