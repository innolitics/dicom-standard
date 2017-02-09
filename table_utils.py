'''
Functions for low-level manipulation of standard tables,
represented by a list-of-lists.

TODO: Figure out duplicated and concatenated row bugs in the 
rowspan expansion.
'''
from bs4 import BeautifulSoup as bs

import parse_relations as pr

def table_to_dict(table, row_names):
    return [dict(zip(row_names, row)) for row in table]

def stringify_table(table):
    return [[str(cell) for cell in row] for row in table]

def tdiv_to_table_list(table_div):
    rows = pr.table_rows(table_div)
    table = [tr_to_row_list(row) for row in rows]
    return table

def tr_to_row_list(tr):
    cells = tr.find_all('td')
    return cells


def expand_spans(table):
    rowwise_expanded_table = expand_rows(table)
    fully_expanded_table = [expand_columns_in_row(row) for row in rowwise_expanded_table]
    return fully_expanded_table


def expand_rows(table):
    '''
    We can't perform a more graceful iteration through the table
    (i.e. a map or comprehension) because information must be
    communicated between each row (the rowspan information).
    '''
    extended_table = []
    row_expansion = [] # Format: [(bs_html_object, row_index)]
    for row in table:
        expanded_row, row_expansion = expand_rowspans(row, row_expansion)
        extended_table.append(expanded_row)
    return extended_table

def expand_rowspans(row, row_expansion):
    updated_row = apply_rowspans_from_prev_row(row, row_expansion)
    row_expansion = update_row_expansion_counter(updated_row, row_expansion)
    return updated_row, row_expansion

def apply_rowspans_from_prev_row(row, row_expansion):
    updated_row = row
    for cell, cell_idx in row_expansion:
        cell = decrement_rowspan_counter(cell)
        updated_row = add_row_cell(updated_row, cell, cell_idx)
    return updated_row

def add_row_cell(row, cell, cell_idx):
    updated_row = slide_down(cell_idx, row)
    updated_row[cell_idx] = cell
    return updated_row

def slide_down(start_idx, row, num_slides=1):
    '''
    Move elements of array `row` down by `num_slides` number of spaces,
    starting at index `start_idx`. Fills the spaces with None.
    '''
    try:
        sliding_rows = row[start_idx:len(row)]
        new_row = row[0:len(row)-len(sliding_rows)]
        for i in range(num_slides):
            new_row.append(None)
        new_row.extend(sliding_rows)
        return new_row
    except IndexError:
        raise ValueError('Cell spans beyond table!')

def decrement_rowspan_counter(cell):
    if int(cell['rowspan']) >= 2:
        cell['rowspan'] = int(cell['rowspan']) - 1
    return cell

def update_row_expansion_counter(row, row_expansion):
    row_expansion = remove_completed_rowspans(row_expansion)
    for idx, cell in enumerate(row):
        if is_new_rowspan_cell(cell, idx, row_expansion):
            row_expansion.append((cell, idx))
    return row_expansion

def is_new_rowspan_cell(cell, idx, row_expansion):
    is_not_recorded = (cell, idx) not in row_expansion
    return has_rowspans_to_expand(cell) and is_not_recorded

def remove_completed_rowspans(row_expansion):
    return [(cell,idx) for (cell, idx) in row_expansion
            if has_rowspans_to_expand(cell)]

def has_rowspans_to_expand(cell):
    rowspan_attr = cell.get('rowspan')
    return int(cell.get('rowspan')) > 1 if rowspan_attr is not None else None


def expand_columns(table):
    return [expand_columns_in_row(row) for row in table]

def expand_columns_in_row(row):
    expanded_cells = map(expand_cell_colspan, row)
    return [cell for span_of_cells in expanded_cells
            for cell in span_of_cells]

def expand_cell_colspan(cell):
    colspan_count = cell.get('colspan')
    expanded_cell = [cell]
    if colspan_count is not None:
        colspans = int(colspan_count)
        cell['colspan'] = 1
        for i in range(colspans-1):
            expanded_cell.append(None)
    return expanded_cell
