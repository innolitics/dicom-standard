'''
Functions for low-level manipulation of standard tables,
represented by a list-of-lists.
'''
from typing import List, Tuple, Dict
from copy import copy
from bs4 import Tag

from dicom_standard import parse_relations as pr

TableListType = List[List[Tag]]
AttributeDictType = Dict[str, str]


def table_to_dict(table: TableListType, row_names: List[str], omit_empty: bool = False) -> List[Dict[str, List[Tag]]]:
    if omit_empty:
        return [dict((k, v) for k, v in zip(row_names, row) if v) for row in table]
    return [dict(zip(row_names, row)) for row in table]


def stringify_table(table: TableListType) -> List[List[str]]:
    return [[str(cell) for cell in row] for row in table]


def tdiv_to_table_list(table_div: Tag) -> List[List[Tag]]:
    rows = pr.table_rows(table_div)
    table_cells = [row.find_all('td') for row in rows if row.find_all('td')]
    # We must also include `th` elements during table parsing to compensate
    # for HTML errors in the DICOM standard.
    table_headers = [row.find_all('th') for row in rows if row.find_all('th')]
    return table_cells + table_headers


def expand_spans(table: TableListType) -> TableListType:
    rowwise_expanded_table = expand_rows(table)
    fully_expanded_table = list(map(expand_columns_in_row, rowwise_expanded_table))
    return fully_expanded_table


def expand_rows(table: TableListType) -> TableListType:
    '''
    We can't perform a more graceful iteration through the table
    (i.e. a map or comprehension) because information must be
    communicated between each row (the rowspan information).
    '''
    extended_table = []
    row_expansion = []  # Format: [(bs_html_object, row_index)]
    for row in table:
        expanded_row, row_expansion = expand_rowspans(row, row_expansion)
        extended_table.append(expanded_row)
    return extended_table


def expand_rowspans(row: List[Tag], row_expansion: List[Tuple[Tag, int]]) -> Tuple[List[Tag], List[Tuple[Tag, int]]]:
    updated_row = apply_rowspans_from_prev_row(row, row_expansion)
    row_expansion = update_row_expansion_counter(updated_row, row_expansion)
    return updated_row, row_expansion


def apply_rowspans_from_prev_row(row: List[Tag], row_expansion: List[Tuple[Tag, int]]) -> List[Tag]:
    updated_row = row
    for cell, cell_idx in row_expansion:
        cell = decrement_rowspan_counter(cell)
        updated_row = add_row_cell(updated_row, cell, cell_idx)
    return updated_row


def add_row_cell(row: List[Tag], cell: Tag, cell_idx: int) -> List[Tag]:
    updated_row = slide_down(cell_idx, row)
    updated_row[cell_idx] = cell
    return updated_row


def slide_down(start_idx: int, row: List[Tag], num_slides: int = 1) -> List[Tag]:
    '''
    Move elements of array `row` down by `num_slides` number of spaces,
    starting at index `start_idx`. Fills the spaces with None.
    '''
    try:
        sliding_rows = row[start_idx:len(row)]
        new_row = row[0:len(row) - len(sliding_rows)]
        for i in range(num_slides):
            new_row.append(None)
        new_row.extend(sliding_rows)
        return new_row
    except IndexError:
        raise ValueError('Cell spans beyond table!')


def decrement_rowspan_counter(cell: Tag) -> Tag:
    if int(cell['rowspan']) >= 2:
        cell['rowspan'] = int(cell['rowspan']) - 1
    return cell


def clear_rowspan_counter(cell: Tag) -> None:
    cell['rowspan'] = 1


def update_row_expansion_counter(row: List[Tag], row_expansion: List[Tuple[Tag, int]]) -> List[Tuple[Tag, int]]:
    row_expansion = remove_completed_rowspans(row_expansion)
    for idx, cell in enumerate(row):
        if is_new_rowspan_cell(cell, idx, row_expansion):
            row_expansion.append((copy(cell), idx))
            clear_rowspan_counter(cell)
    return row_expansion


def is_new_rowspan_cell(cell: Tag, idx: int, row_expansion: List[Tuple[Tag, int]]) -> bool:
    is_not_recorded = (cell, idx) not in row_expansion
    return has_rowspans_to_expand(cell) and is_not_recorded


def remove_completed_rowspans(row_expansion: List[Tuple[Tag, int]]) -> List[Tuple[Tag, int]]:
    return [(cell, idx) for (cell, idx) in row_expansion
            if has_rowspans_to_expand(cell)]


def has_rowspans_to_expand(cell: Tag) -> bool:
    rowspan_attr = cell.get('rowspan')
    return int(cell.get('rowspan')) > 1 if rowspan_attr is not None else None


def expand_columns_in_row(row: List[Tag]) -> List[Tag]:
    expanded_cells = map(expand_cell_colspan, row)
    return [cell for span_of_cells in expanded_cells
            for cell in span_of_cells]


def expand_cell_colspan(cell: Tag) -> Tag:
    colspan_count = cell.get('colspan')
    expanded_cell = [cell]
    if colspan_count is not None:
        colspans = int(colspan_count)
        cell['colspan'] = 1
        for i in range(colspans - 1):
            expanded_cell.append(None)
    return expanded_cell
