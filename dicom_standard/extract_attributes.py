'''
Extract the listing of all attributes given in PS3.6 of the DICOM Standard.
'''
from typing import List
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.table_utils import TableDictType, get_tables_from_ids

COLUMN_TITLES = ['tag', 'name', 'keyword', 'valueRepresentation', 'valueMultiplicity', 'retired']
TABLE_IDS = ['table_6-1', 'table_7-1', 'table_8-1', 'table_9-1']


# TODO: Convert attributes to a TypedDict when we update to use Python3.8
def attribute_table_to_json(table: List[TableDictType]) -> List[TableDictType]:
    attributes = []
    for attr in table:
        attr['id'] = pl.create_slug(attr['tag'])
        attr['tag'] = attr['tag'].upper()
        attr['retired'] = 'Y' if 'RET' in attr['retired'] else 'N'
        attributes.append(attr)
    return attributes


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table = get_tables_from_ids(standard, TABLE_IDS, COLUMN_TITLES)
    parsed_table_data = attribute_table_to_json(table)
    pl.write_pretty_json(parsed_table_data)
