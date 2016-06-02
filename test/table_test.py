from bs4 import BeautifulSoup
import pandas as pd

from html_snippets import *
import parse_lib as pl

def test_flat():
    table = BeautifulSoup(flat, 'html.parser')
    df = pl.table_to_dataframe(table)
    expected_df = pd.DataFrame(
            {'IE': ['<td>1</td>', '<td>1</td>', '<td>1</td>'],
             'Module': ['<td>2</td>', '<td>2</td>', '<td>2</td>'],
             'Reference': ['<td>3</td>', '<td>3</td>', '<td>3</td>'],
             'Usage': ['<td>4</td>', '<td>4</td>', '<td>4</td>']
             })
    assert df.equals(expected_df)

def test_with_links():
    table = BeautifulSoup(with_links, 'html.parser')
    df = pl.table_to_dataframe(table)
    expected_df = pd.DataFrame(
            {'IE': ['<td><a href="somelink">1</a></td>', '<td><a href="somelink">1</a></td>', '<td><a href="somelink">1</a></td>'],
             'Module': ['<td>2</td>', '<td>2</td>', '<td>2</td>'],
             'Reference': ['<td>3</td>', '<td>3</td>', '<td>3</td>'],
             'Usage': ['<td>4</td>', '<td>4</td>', '<td>4</td>']
             })
    assert df.equals(expected_df)

def test_rowspan():
    table = BeautifulSoup(rowspan, 'html.parser')
    df = pl.table_to_dataframe(table)
    expected_df = pd.DataFrame(
            {'IE': ['<td rowspan="3"><a href="somelink">1</a></td>', '<td>2</td>', '<td>2</td>'],
             'Module': ['<td>2</td>', '<td>3</td>', '<td>3</td>'],
             'Reference': ['<td>3</td>', '<td>4</td>', '<td>4</td>'],
             'Usage': ['<td>4</td>', None, None]
             })
             
    assert df.equals(expected_df)

def test_colspan():
    table = BeautifulSoup(colspan, 'html.parser')
    df = pl.table_to_dataframe(table)
    expected_df = pd.DataFrame(
            {'IE': ['<td colspan="3"><a href="somelink">1</a></td>', '<td>1</td>', '<td>1</td>'],
             'Module': ['<td>4</td>', '<td>2</td>', '<td>2</td>'],
             'Reference': [None, '<td>3</td>', '<td>3</td>'],
             'Usage': [None, '<td>4</td>', '<td>4</td>']
             })
    print(df)
    print(expected_df)
    assert df.equals(expected_df)

def test_slide():
    row = pd.Series([1., 2., None, None])
    start_idx = 0
    num_slides = 2
    row = pl.slide_down_col(start_idx, num_slides, row)
    row = pd.Series(row)
    expected_row = pd.Series([1., 2., None, 2.])
    assert row.equals(expected_row)

def test_get_td_html():
    tag = '<td align="left" rowspan="2" colspan="1">This is <a href="content_link">some content</a> I want.</td>'
    content = pl.get_td_html_content(tag)
    assert content == 'This is <a href="content_link">some content</a> I want.'

def test_expand_colspan():
    table = BeautifulSoup(colspan, 'html.parser')
    df = pl.table_to_dataframe(table)
    df = pl.expand_colspan(df)
    expected_df = pd.DataFrame(
            {'IE': ['<a href="somelink">1</a>', '1', '1'],
             'Module': ['<a href="somelink">1</a>', '2', '2'],
             'Reference': ['<a href="somelink">1</a>', '3', '3'],
             'Usage': ['4', '4', '4']
             })
    print(df)
    print(expected_df)
    assert df.equals(expected_df)
