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
REFERENCE_COLUMN = 2

def get_json_from_standard(standard_path, json_path, mode):
    '''
    Given a section of the standard, parse the HTML tables and return the data
    in a JSON file.
    '''
    chapter_name, match_pattern, column_titles, column_correction = get_table_headers_and_location(mode)
    with open(standard_path, 'r') as standard_file, open(json_path, 'w') as output_json_rough:
        standard = BeautifulSoup(standard_file, 'html.parser')
        all_tables = standard.find_all('div', class_='table')
        chapter_tables = get_all_tdivs_from_chapter(standard, chapter_name)
        for tdiv in chapter_tables:
            table_name = tdiv.p.strong.get_text()
            if match_pattern.match(table_name):
                final_table = condition_table_data(tdiv, all_tables, column_correction)
                json_list = table_to_json(final_table, column_titles, table_name)
                output_json_rough.write(json.dumps(json_list, sort_keys=False, indent=4, separators=(',',':')) + ", \n")

def get_table_headers_and_location(mode):
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
    return (chapter_name, match_pattern, column_titles, column_correction)

def get_all_tdivs_from_chapter(standard, chapter_name):
    table_divs = []
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if chapter.div.div.div.h1.a.get('id') == chapter_name:
            table_divs = chapter.find_all('div', class_='table')
            return table_divs

def condition_table_data(tdiv, all_tables, column_correction):
    table_body = tdiv.div.table.tbody
    raw_table = table_to_list(tdiv, all_tables)
    full_table = expand_spans(raw_table)
    if column_correction:
        full_table = correct_for_missing_type_column(full_table) 
    link_correction = not column_correction
    final_table = extract_text_from_html(full_table, link_correction)
    return final_table

def correct_for_missing_type_column(full_table):
    '''
    Corrects for the attribute tables which sometimes do not have the type
    column in the HTML version of the standard.
    '''
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

def get_spans(table):
    '''
    Find all rowspans and colspans in an HTML table. Returns a 2D list of
    tuples of the form (rowspan value, colspan value, html content)
    '''
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

def table_to_list(table_div, macro_table_list=None):
    '''
    Converts an HTML table to a 2D list, expanding macros along the way.
    '''
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
        macro_div = find_table_div(macro_table_list, table_id)
        macro_table = table_to_list(macro_div, macro_table_list)
        return macro_table
    return None

def find_table_div(all_tables, table_id):
    try:
        for table in all_tables:
            if (table.a.get('id') == table_id):
                return table
        return None
    except AttributeError:
        return None

def extract_text_from_html(full_table, link_correction):
    final_table = []
    for row in full_table:
        temp_row = []
        for i in range(len(row)):
            temp_row.append(get_text_or_href_from_cell(row[i], i, link_correction))
        final_table.append(temp_row)
    return final_table

def get_text_or_href_from_cell(cell_html, column_idx, link_correction):
    if cell_html is None:
        return None
    html = BeautifulSoup(cell_html, 'html.parser')
    if column_idx == REFERENCE_COLUMN and link_correction:
        id_sequence, ref_link = html.find_all('a')
        return ref_link.get('href')
    else:
        return html.get_text()

def table_to_json(final_table, column_titles, table_name):
    '''
    Convert a single table to a JSON dictionary. 
    '''
    col1, col2, col3, col4 = zip(*final_table)
    table_data = []
    for c1, c2, c3, c4 in zip(col1, col2, col3, col4):
        table_data.append({column_titles[0]: c1, column_titles[1]: c2, column_titles[2]: c3, column_titles[3]: c4})
    json_list = {
        'tableName': table_name,
        'tableData': table_data
    }
    return json_list

