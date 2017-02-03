'''
Functions for low-level manipulation of standard tables,
represented by a list-of-lists.

TODO: Figure out duplicated and concatenated row bugs in the 
colspan expansion.
'''
from bs4 import BeautifulSoup as bs

# print([row for row in columnwise_expanded_table if len(row) > 4])

def table_to_dict(table, column_names):
    return [dict(zip(column_names, row)) for row in table]

def stringify_table(table):
    return [[str(cell) for cell in row] for row in table]

def expand_spans(table):
    columnwise_expanded_table = expand_columns(table)
    fully_expanded_table = [expand_row(row) for row in columnwise_expanded_table]
    return fully_expanded_table


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
        extended_table.append(expanded_row)
    return extended_table

def expand_colspans(row, column_expansion):
    updated_row = apply_colspans_from_prev_row(row, column_expansion)
    column_expansion = update_column_expansion_counter(updated_row, column_expansion)
    return updated_row, column_expansion

def apply_colspans_from_prev_row(row, column_expansion):
    updated_row = row
    for cell, cell_idx in column_expansion:
        cell = decrement_colspan_counter(cell)
        updated_row = add_column_cell(updated_row, cell, cell_idx)
    return updated_row

def add_column_cell(row, cell, cell_idx):
    updated_row = slide_down(cell_idx, row)
    updated_row[cell_idx] = cell
    return updated_row

def slide_down(start_idx, row, num_slides=1):
    '''
    Move elements of array `row` down by `num_slides` number of spaces,
    starting at index `start_idx`. Fills the spaces with None.
    '''
    try:
        sliding_columns = row[start_idx:len(row)]
        new_row = row[0:len(row)-len(sliding_columns)]
        for i in range(num_slides):
            new_row.append(None)
        new_row.extend(sliding_columns)
        return new_row
    except IndexError:
        raise ValueError('Cell spans beyond table!')

def decrement_colspan_counter(cell):
    if int(cell['colspan']) >= 2:
        cell['colspan'] = int(cell['colspan']) - 1
    return cell

def update_column_expansion_counter(row, column_expansion):
    column_expansion = remove_completed_colspans(column_expansion)
    for idx, cell in enumerate(row):
        if is_new_colspan_cell(cell, idx, column_expansion):
            column_expansion.append((cell, idx))
    return column_expansion

def is_new_colspan_cell(cell, idx, column_expansion):
    is_not_recorded = (cell, idx) not in column_expansion
    return has_colspans_to_expand(cell) and is_not_recorded

def remove_completed_colspans(column_expansion):
    return [(cell,idx) for (cell, idx) in column_expansion
            if has_colspans_to_expand(cell)]

def has_colspans_to_expand(cell):
    return int(cell.get('colspan')) > 1


def expand_row(row):
    expanded_cells = map(expand_cell_rowspan, row)
    return [cell for span_of_cells in expanded_cells
            for cell in span_of_cells]

def expand_cell_rowspan(cell):
    rowspans = int(cell.get('rowspan'))
    cell['rowspan'] = 1
    expanded_cell = [cell]
    for i in range(rowspans-1):
        expanded_cell.append(None)
    return expanded_cell
