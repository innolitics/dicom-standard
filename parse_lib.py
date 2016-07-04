'''
Common functions for extracting information from the
DICOM standard HTML file.
'''

import json
import re
from copy import deepcopy

from bs4 import BeautifulSoup, NavigableString

FULL_TABLE_COLUMN_NUM = 4
REFERENCE_COLUMN = 2

def ciod_module_data_from_standard(standard):
    chapter_name = "chapter_A"
    match_pattern = re.compile(".*IOD Modules$")
    column_titles = ['information_entity', 'module', 'link_to_standard', 'usage']
    column_correction = False
    return table_data_from_standard(standard, chapter_name, match_pattern,
                                    column_titles, column_correction)

def module_attribute_data_from_standard(standard):
    chapter_name = "chapter_C"
    match_pattern = re.compile("(.*Module Attributes$)|(.*Module Table$)")
    column_titles = ['name', 'tag', 'type', 'description']
    column_correction = True
    return table_data_from_standard(standard, chapter_name, match_pattern,
                                    column_titles, column_correction)

def table_data_from_standard(standard, chapter_name, match_pattern, column_titles, column_correction):
    '''
    Given a section of the standard, parse the HTML tables and return the data
    in a JSON file.
    '''
    all_tables = standard.find_all('div', class_='table')
    chapter_tables = all_tdivs_in_chapter(standard, chapter_name)
    all_table_dicts = []
    for tdiv in chapter_tables:
        table_name = tdiv.p.strong.get_text()
        table_id = tdiv.a.get('id')
        if match_pattern.match(table_name):
            final_table = condition_table_data(tdiv, all_tables, column_correction)
            all_table_dicts.append(table_to_dict(final_table, column_titles, table_name, table_id))
    return all_table_dicts

def all_tdivs_in_chapter(standard, chapter_name):
    table_divs = []
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if chapter.div.div.div.h1.a.get('id') == chapter_name:
            table_divs = chapter.find_all('div', class_='table')
            return table_divs

def clean_table_name(name):
    table, section, title = re.split('\u00a0', name)
    clean_title, *splits = re.split('(IOD Modules)|(Module Attributes)|(Macro Attributes)|(Module Table)', title)
    return clean_title.strip()

def clean_table_entry(name):
    clean_title, *splits = re.split('Module', name)
    return clean_title.strip()

def create_slug(title):
    first_pass_slugify = title.lower().replace(" ", "-").replace(",", "-")
    return re.sub('(\()|(\))', '', first_pass_slugify)

def condition_table_data(tdiv, all_tables, column_correction):
    raw_table = table_to_list(tdiv, all_tables)
    full_table = expand_spans(raw_table)
    if column_correction:
        full_table = correct_for_missing_type_column(full_table)
    link_correction = not column_correction
    text_table_with_newlines = extract_text_from_html(full_table, link_correction)
    final_table = [map(remove_stray_newlines, row) for row in text_table_with_newlines]
    return final_table

def remove_stray_newlines(attribute_value):
    if isinstance(attribute_value, str):
        return attribute_value.replace('\n', '')
    else:
        return attribute_value

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

def find_spans(table):
    '''
    Find all rowspans and colspans in an HTML table. Returns a 2D list of
    tuples of the form (rowspan value, colspan value, html content)
    '''
    spans = []
    for row in table:
        row_spans = []
        for cell in row:
            cell_span = span_from_cell(cell)
            row_spans.append(cell_span)
        spans.append(row_spans)
    return spans

def span_from_cell(cell):
    if cell is None:
        return None
    cell_html = BeautifulSoup(cell, 'html.parser')
    td_tag = cell_html.find('td')
    cell_span = [
        int(td_tag.get('rowspan', 1)),
        int(td_tag.get('colspan', 1)),
        td_html_content(str(td_tag))
    ]
    return cell_span

def td_html_content(td_html):
    split_html = re.split('(<td.*?>)|(</td>)', td_html)
    return split_html[3]

def expand_spans(table):
    '''
    Fills in tables by unpacking rowspans and colspans. Results in a
    table with an equal number of cells in each row.
    '''
    expanded_table = []
    spans = find_spans(table)
    for i in range(len(table)):
        row = []
        for j in range(len(table[i])):
            spans, html = expand_span_in_cell(spans, i, j)
            row.append(html)
        expanded_table.append(row)
    return expanded_table

def expand_span_in_cell(spans, i, j):
    if spans[i][j] is None:
        return spans, None
    else:
        rowspan, colspan, html = spans[i][j]
        if rowspan > 1:
            spans = expand_rowspan(spans, i, j)
        if colspan > 1:
            spans = expand_colspan(spans, i, j)
        return spans, html

def expand_rowspan(spans, i, j):
    row_slides = spans[i][j][0] - 1
    spans[i][j][0] = 1
    for k in range(1, row_slides+1):
        spans[i+k] = slide_down(j-1, 1, spans[i+k])
        spans[i+k][j] = deepcopy(spans[i][j])
    return spans

def expand_colspan(spans, i, j):
    col_slides = spans[i][j][1] - 1
    spans[i][j][1] = 1
    spans[i] = slide_down(j, col_slides, spans[i])
    for k in range(1, col_slides+1):
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
    for row in table_body.find_all('tr'):
        macro_reference = check_for_macros(row, macro_table_list, current_table_id)
        if macro_reference is not None:
            table.extend(macro_reference)
            continue
        cells = convert_row_to_list(row)
        table.append(cells)
    return table

def convert_row_to_list(row):
    cells = []
    all_cells_in_row = row.find_all('td')
    for cell in all_cells_in_row:
        cells.append(str(cell))
    for j in range(len(cells), 4):
        cells.append(None)
    return cells

def check_for_macros(row, macro_table_list, current_table_id):
    if macro_table_list is not None:
        all_cells_in_row = row.find_all('td')
        cell = all_cells_in_row[0]
        specified_macro = None
        if is_macro_link(cell):
            specified_macro = macro_expansion(cell, current_table_id, macro_table_list)
        if specified_macro is not None:
            return specified_macro
    return None

def is_macro_link(cell):
    link_pattern = re.compile('.*Include.*')
    try:
        has_link = cell.p.span.a is not None
        link_is_include = link_pattern.match(cell.p.span.get_text()) is not None
        return has_link and link_is_include
    except AttributeError:
        return False

def macro_expansion(cell, current_table_id, macro_table_list):
    if is_macro_link(cell):
        table_id = extract_referenced_table_id(cell)
        if table_id == current_table_id:
            return None
        macro_div = find_table_div(macro_table_list, table_id)
        macro_table = table_to_list(macro_div, macro_table_list)
        prepend_sequence_indicators(cell, macro_table)
        return macro_table
    return None

def extract_referenced_table_id(cell):
    link = cell.p.span.a.get('href')
    _url, _pound, table_id = link.partition('#')
    if table_id is None:
        raise ValueError("Formatting error")
    return table_id

def find_table_div(all_tables, table_id):
    try:
        for table in all_tables:
            if table.a.get('id') == table_id:
                return table
        return None
    except AttributeError:
        return None

def prepend_sequence_indicators(cell, macro_table):
    if macro_table is None:
        return
    indicator = sequence_indicator_from_cell(cell.p.span.get_text())
    for row in macro_table:
        row[0] = insert_indicator_into_html(indicator, row[0])

def insert_indicator_into_html(indicator, html):
    name_cell = BeautifulSoup(html, 'html.parser').find('td')
    name_cell.insert(0, NavigableString(indicator))
    return str(name_cell)

def sequence_indicator_from_cell(cell):
    preceding_space, *split = re.split('^(>+)', cell)
    if split == []:
        indicator = ''
    else:
        indicator = split[0]
    return indicator

def extract_text_from_html(full_table, link_correction):
    final_table = []
    for row in full_table:
        temp_row = []
        for i in range(len(row)):
            temp_row.append(text_or_href_from_cell(row[i], i, link_correction))
        final_table.append(temp_row)
    return final_table

def text_or_href_from_cell(cell_html, column_idx, link_correction):
    if cell_html is None:
        return None
    html = BeautifulSoup(cell_html, 'html.parser')
    if column_idx == REFERENCE_COLUMN and link_correction:
        id_sequence, ref_link = html.find_all('a')
        return ref_link.get('href')
    else:
        return clean_table_entry(html.get_text())

def table_to_dict(final_table, column_titles, table_name, table_id):
    '''
    Convert a single table to a dictionary.
    '''
    col1, col2, col3, col4 = zip(*final_table)
    clean_name = clean_table_name(table_name)
    slug = create_slug(clean_name)
    doc_link = find_doc_link(table_id)
    table_data = []
    i = -1
    for cell1, cell2, cell3, cell4 in zip(col1, col2, col3, col4):
        i += 1
        table_data.append({column_titles[0]: cell1, column_titles[1]: cell2,
                           column_titles[2]: cell3, column_titles[3]: cell4,
                           "order": i})
    table_dict = {
        'name': clean_name,
        'data': table_data,
        'slug': slug,
        'link_to_standard': doc_link
    }
    return table_dict

def find_doc_link(table_id):
    url_prefix = "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#"
    return url_prefix + table_id

def parse_html_file(filepath):
    with open(filepath, 'r') as html_file:
        return BeautifulSoup(html_file, 'html.parser')

def dump_pretty_json(filepath, write_status, data, prefix=None):
    with open(filepath, write_status) as json_file:
        if prefix is not None:
            json_file.write(prefix)
        json.dump(data, json_file, sort_keys=False, indent=4, separators=(',', ':'))

def read_json_to_dict(filepath):
    with open(filepath, 'r') as json_file:
        json_string = json_file.read()
        json_dict = json.loads(json_string)
        return json_dict

def left_join(list_of_dicts, dict_of_dicts, left_key):
    joined = []
    for left_row in list_of_dicts:
        key_value = left_row[left_key]
        try:
            right_row = dict_of_dicts[key_value]
        except KeyError as e:
            print(left_row, e)
            raise e
        joined.append({**left_row, **right_row})
    return joined
