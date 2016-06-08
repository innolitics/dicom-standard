'''
parse_lib.py

Common functions for extracting information from the 
DICOM standard HTML file.
'''

import json
import re
from copy import deepcopy

from bs4 import BeautifulSoup

FULL_TABLE_COLUMN_NUM = 4

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

def table_to_list(table_div, macro_table_list=None):
    if table_div is None:
        return None
    current_table_id = table_div.a.get('id')
    table = []
    table_body = table_div.find('tbody') 
    rows = table_body.find_all('tr')
    for row in table_body.find_all('tr'):
        cells = []
        cell_html = row.find_all('td')
        if (macro_table_list is not None):
            specified_macro = macro_expansion(cell_html, current_table_id, macro_table_list)
            if specified_macro is not None:
                table.extend(specified_macro)
                continue
        for cell in cell_html:
            cells.append(str(cell))
        for j in range(len(cells), 4):
            cells.append(None)
        table.append(cells)
    return table

def is_macro_link(cell):
    link_pattern = re.compile('.*Include.*')
    try:
        has_link = cell.p.span.a is not None
        link_is_include = link_pattern.match(cell.p.span.get_text()) is not None
        return has_link and link_is_include
    except AttributeError:
        return False
    
def macro_expansion(row, current_table_id, macro_table_list):
    if is_macro_link(row[0]):
        link = row[0].p.span.a.get('href')
        _url, _pound, table_id = link.partition('#')
        if table_id is None:
            raise ValueError("URL formatting error")
        if table_id == current_table_id:
            return None
        macro_div = find_sub_table_div(macro_table_list, table_id)
        macro_table = table_to_list(macro_div, macro_table_list)
        return macro_table
    return None

def get_spans(table):
    spans = []
    for row in table:
        row_spans = []
        for cell in row:
            if cell is None:
                row_spans.append(None)
                continue
            cell_html = BeautifulSoup(cell, 'html.parser')
            td = cell_html.find('td')
            cell_span = [
                int(td.get('rowspan', 1)),
                int(td.get('colspan', 1)),
                get_td_html_content(str(td))
            ]
            row_spans.append(cell_span) 
        spans.append(row_spans)
    return spans

def get_td_html_content(td_html):
    split_html = re.split('(<td.*?>)|(</td>)', td_html)
    return split_html[3]

def slide_down(start_idx, num_slides, row):
    ''' 
    Moves cells down a row or column by num_slides positions starting 
    after index start_idx. Used to make room for rowspan and colspan
    unpacking.
    ''' 
    try:
        sliding_columns = row[start_idx+1:len(row)-num_slides]
        new_row = row[0:len(row)-len(sliding_columns)]
        new_row.extend(sliding_columns)
        return new_row 
    except IndexError:
        raise ValueError('Cell spans beyond table!') 

def expand_spans(table):
    '''
    Fills in tables by unpacking rowspans and colspans. Results in a
    table with an equal number of cells in each row.
    '''
    expanded_table = [] 
    spans = get_spans(table)
    for i in range(len(table)):
        row = []
        for j in range(len(table[i])):
            if spans[i][j] is None:
                row.append(None)
            else:
                rowspan, colspan, html = spans[i][j]
                row.append(html) 
                if (rowspan > 1):
                    spans = expand_rowspan(spans, i, j)
                if (colspan > 1):
                    spans = expand_colspan(spans, i, j)
        expanded_table.append(row)
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

def standard_tables_to_json(standard_path, json_path, mode):
    chapter_name = None 
    match_pattern = None
    column_titles = []
    column_correction = False
    if mode == 'ciods':
        chapter_name = "chapter_A"
        match_pattern = re.compile(".*IOD Modules$")
        column_titles = ['IE Name', 'Module', 'Doc Reference', 'Usage']
    elif mode == 'modules':
        chapter_name = "chapter_C"
        match_pattern = re.compile(".*Module Attributes$")
        column_titles = ['Attribute', 'Tag', 'Type', 'Description']
        column_correction = True
    else:
        raise ValueError('Invalid mode')
    with open(standard_path, 'r') as standard_file, open(json_path, 'w') as output_json_rough:
        standard = BeautifulSoup(standard_file, 'html.parser')
        all_tables = standard.find_all('div', class_='table')
        chapter_tables = get_chapter_table_divs(standard, chapter_name)
        for tdiv in chapter_tables:
            table_name = tdiv.p.strong.get_text()
            if match_pattern.match(table_name):
                table_body = tdiv.div.table.tbody
                raw_table = table_to_list(tdiv, all_tables)
                full_table = expand_spans(raw_table)
                if column_correction:
                    full_table = correct_for_missing_type_column(full_table) 
                col1, col2, col3, col4 = zip(*full_table)
                table_data = []
                for c1, c2, c3, c4 in zip(col1, col2, col3, col4):
                    table_data.append({column_titles[0]: c1, column_titles[1]: c2, column_titles[2]: c3, column_titles[3]: c4})
                json_list = [{
                    'tableName': table_name,
                    'tableData': table_data
                }]
                output_json_rough.write(json.dumps(json_list, sort_keys=False, indent=4, separators=(',',':')) + "\n")

def correct_for_missing_type_column(full_table):
    corrected_table = []
    for a_name, a_tag, a_type, a_descr in full_table:
        corrected_row = [a_name, a_tag]
        if a_descr is None:
            a_corrected_type = a_descr
            a_corrected_descr = a_type
            corrected_row.extend([a_corrected_type, a_corrected_descr])
        else:
            corrected_row.extend([a_type, a_descr])
        corrected_table.append(corrected_row)
    return corrected_table
