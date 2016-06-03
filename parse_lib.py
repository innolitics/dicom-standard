'''
parse_lib.py

Common functions for extracting information from the 
DICOM standard HTML file.
'''

import re
from copy import deepcopy

from bs4 import BeautifulSoup

def find_sub_table_div(all_tables, table_id):
    try:
        for table in all_tables:
            if (table.a.get('id') == table_id):
                return table
        return None
    except AttributeError:
        return None

def extract_doc_links(table_body):
    data = []
    links = table_body.find_all('a')
    for link in links:
        if link.get('href'):
            data.append(link.get('href'))
    return data

def get_table_headers(table_div):
    headers = []
    cols = table_div.find_all('th')
    for col in cols:
        headers.append(col.get_text())
    if len(headers) == 3: # TODO: clearer way to state this?
        headers.append(headers[2])
        headers[2] = "Type"
    return headers

def table_to_list(table_div, all_tables=None):
    if table_div is None:
        return None
    current_table_id = table_div.a.get('id')
    table = []
    column_headers = get_table_headers(table_div)
    table_body = table_div.find('tbody') 
    rows = table_body.find_all('tr')
    for i in range(len(rows)):
        cells = []
        cell_objs = rows[i].find_all('td')
        if (all_tables is not None):
            macro = macro_expansion(cell_objs, current_table_id, all_tables)
            if macro is not None:
                table.extend(macro)
                continue
        for cell_obj in cell_objs:
            cells.append(str(cell_obj))
        for j in range(len(cells),len(column_headers)):
            cells.append(None)
        table.append(cells)
    return table

def macro_link(cell):
    link_pattern = re.compile('.*Include.*')
    try:
        return cell.p.span.a is not None and link_pattern.match(cell.p.span.get_text()) is not None
    except AttributeError:
            return False
    
def macro_expansion(row, current_table_id, all_tables):
    if macro_link(row[0]):
        link = row[0].p.span.a.get('href')
        _url, _pound, table_id = link.partition('#')
        if table_id is None:
            raise ValueError("URL formatting error")
        if table_id == current_table_id:
            return None
        macro_div = find_sub_table_div(all_tables, table_id)
        macro_table = table_to_list(macro_div, all_tables)
        return macro_table
    return None

def get_spans(table):
    spans = [[None for col in row] for row in table]
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] is None:
                spans[i][j] = None
                continue
            cell = BeautifulSoup(table[i][j], 'html.parser')
            td = cell.find('td')
            cell_span = [1, 1, get_td_html_content(str(td))]
            if td.has_attr('rowspan'):
                cell_span[0] = int(td.get('rowspan'))
            if td.has_attr('colspan'):
                cell_span[1] = int(td.get('colspan'))
            spans[i][j] = cell_span
    return spans

def get_td_html_content(td_html):
    split_html = re.split('(<td.*?>)|(</td>)', td_html)
    return split_html[3]

def slide_down(start_idx, num_slides, row):
    try:
        sliding_columns = row[start_idx+1:len(row)-num_slides]
        row = row[0:len(row)-len(sliding_columns)]
        row.extend(sliding_columns)
        return row 
    except IndexError:
        raise ValueError('Cell spans beyond table!') 

def expand_spans(table):
    expanded_table = [[None for col in row] for row in table]
    spans = get_spans(table)
    for i in range(len(table)):
        for j in range(len(table[i])):
            if spans[i][j] is not None:
                expanded_table[i][j]  = spans[i][j][2]
                if (spans[i][j][0] > 1):
                    spans = expand_rowspan(spans, i, j)
                if (spans[i][j][1] > 1):
                    spans = expand_colspan(spans, i, j)
    return expanded_table 

def expand_rowspan(spans, i, j):
    row_slides = spans[i][j][0] - 1
    spans[i][j][0] = 1
    for k in range(1,row_slides+1):
        spans[i+k] = slide_down(j-1, 1, spans[i+k])
        spans[i+k][j] = deepcopy(spans[i][j])
    return spans

def expand_colspan(spans, i, j):
    col_slides = spans[i][j][1] - 1
    spans[i][j][1] = 1
    spans[i] = slide_down(j,col_slides,spans[i])
    for k in range(1,col_slides+1):
        spans[i][j+k] = deepcopy(spans[i][j])
    return spans

def extract_table_data(table_body):
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    return data

def get_chapter_table_divs(standard, chapter_name):
    table_divs = []
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if chapter.div.div.div.h1.a.get('id') == chapter_name:
            table_divs = chapter.find_all('div', class_='table')
            return table_divs
