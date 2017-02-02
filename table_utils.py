'''
Functions for low-level manipulation of standard tables,
represented by a list-of-lists.
'''
from bs4 import BeautifulSoup as bs


def expand_spans(table):
    columnwise_expanded_table = expand_columns(table)
    fully_expanded_table = [expand_row(row) for row in columnwise_expanded_table]
    return fully_expanded_table

'''
TODO: complete `expand_row()`
'''

def expand_columns(table):
    '''
    We can't perform a more graceful iteration through the table
    (i.e. a map or comprehension) because information must be
    communicated between each row (the colspan information).
    '''
    extended_table = []
    column_expansion = [] # Format: [(bs_html_object, row_index)]
    for row in table:
        expanded_row, column_expansion = expand_colspans(row, column_expansion)
        expanded_table.append(expanded_row)
    return extended_table

def expand_colspans(row, column_expansion):
    updated_row = apply_colspans_from_prev_row(row, column_expansion)
    column_expansion = update_column_expansion_counter(updated_row, column_expansion)
    return updated_row

def apply_colspans_from_prev_row(row, column_expansion):
    updated_row = row
    for cell, cell_idx in column_expansion:
        cell = decrement_colspan_counter(cell)
        updated_row = add_column_cell(updated_row, cell, cell_idx)
    return updated_row

def add_column_cell(row, cell, cell_idx):
    updated_row = slide_down(cell_idx, row)
    updated_row[cell_idx] = str(cell)
    return updated_row

def decrement_colspan_counter(cell):
    if cell['colspan'] >= 2:
        cell['colspan'] -= 1
    else:
        del cell['colspan']
    return cell

def update_column_expansion_counter(row, column_expansion):
    column_expansion = remove_completed_colspans(column_expansion)
    for cell, idx in enumerate(row):
        parsed_cell = bs(cell, 'html.parser').find('td')
        if is_new_colspan_cell(parsed_cell, idx, column_expansion):
            column_expansion.append((parsed_cell, idx))
    return column_expansion

def is_new_colspan_cell(parsed_cell, idx, column_expansion):
    has_colspan_attr = parsed_cell.get('colspan')
    is_new_colspan_cell = not column_expansion.contains((parsed_cell, idx))
    return has_colspan_attr and is_new_colspan_cell

def remove_completed_colspans(column_expansion):
    for cell_idx_pair in column_expansion:
        if not cell_idx_pair[0].get('colspan'):
            column_expansion.remove(cell_idx_pair)
    return column_expansion

def slide_down(start_idx, row, num_slides=1):
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
