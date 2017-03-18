'''
Functions for low-level manipulation of standard tables,
represented by a list-of-lists.
'''
from copy import copy
from typing import List, Tuple 
from bs4 import BeautifulSoup as bs
from bs4.element import PageElement

import parse_relations as pr

RowExpansionType = List[Tuple[PageElement, int]]

def table_to_dict(table: list, row_names: List[str]) -> List[dict]:
    return [dict(zip(row_names, row)) for row in table]

def stringify_table(table: list) -> List[List[str]]:
    return [[str(cell) for cell in row] for row in table]

def tdiv_to_table_list(table_div: PageElement) -> List[List[PageElement]]:
    rows = pr.table_rows(table_div)
    table = [row.find_all('td') for row in rows]
    return table

def expand_spans(table: List[List[PageElement]]) -> List[List[PageElement]]:
    rowwise_expanded_table = expand_rows(table)
    fully_expanded_table = list(map(expand_columns_in_row, rowwise_expanded_table))
    return fully_expanded_table


def expand_rows(table: List[List[PageElement]]) -> List[List[PageElement]]:
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

def expand_rowspans(row: List[PageElement], row_expansion: RowExpansionType) -> Tuple[List[PageElement], RowExpansionType]:
    updated_row = apply_rowspans_from_prev_row(row, row_expansion)
    row_expansion = update_row_expansion_counter(updated_row, row_expansion)
    return updated_row, row_expansion

def apply_rowspans_from_prev_row(row: List[PageElement], row_expansion: RowExpansionType) -> List[PageElement]:
    updated_row = row
    for cell, cell_idx in row_expansion:
        cell = decrement_rowspan_counter(cell)
        updated_row = add_row_cell(updated_row, cell, cell_idx)
    return updated_row

def add_row_cell(row: List[PageElement], cell: PageElement, cell_idx: int) -> List[PageElement]:
    updated_row = slide_down(cell_idx, row)
    updated_row[cell_idx] = cell
    return updated_row

def slide_down(start_idx: int, row: list, num_slides: int=1) -> list:
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

def decrement_rowspan_counter(cell: PageElement) -> PageElement:
    if int(cell['rowspan']) >= 2:
        cell['rowspan'] = int(cell['rowspan']) - 1
    return cell

def clear_rowspan_counter(cell: PageElement) -> None:
    cell['rowspan'] = 1

def update_row_expansion_counter(row: List[PageElement], row_expansion: RowExpansionType) -> RowExpansionType:
    row_expansion = remove_completed_rowspans(row_expansion)
    for idx, cell in enumerate(row):
        if is_new_rowspan_cell(cell, idx, row_expansion):
            row_expansion.append((copy(cell), idx))
            clear_rowspan_counter(cell)
    return row_expansion

def is_new_rowspan_cell(cell: PageElement, idx: int, row_expansion: RowExpansionType) -> bool:
    is_not_recorded = (cell, idx) not in row_expansion
    return has_rowspans_to_expand(cell) and is_not_recorded

def remove_completed_rowspans(row_expansion: RowExpansionType) -> RowExpansionType:
    return [(cell,idx) for (cell, idx) in row_expansion
            if has_rowspans_to_expand(cell)]

def has_rowspans_to_expand(cell: PageElement) -> bool:
    rowspan_attr = cell.get('rowspan')
    return int(cell.get('rowspan')) > 1 if rowspan_attr is not None else None


def expand_columns_in_row(row: List[PageElement]) -> List[PageElement]:
    expanded_cells = map(expand_cell_colspan, row)
    return [cell for span_of_cells in expanded_cells
            for cell in span_of_cells]

def expand_cell_colspan(cell: PageElement) -> List[PageElement]:
    colspan_count = cell.get('colspan')
    expanded_cell = [cell]
    if colspan_count is not None:
        colspans = int(colspan_count)
        cell['colspan'] = 1
        for i in range(colspans-1):
            expanded_cell.append(None)
    return expanded_cell
