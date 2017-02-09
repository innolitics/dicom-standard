'''
Extract the listing of all attributes given in PS3.6 of the DICOM Standard.
'''
import sys

import parse_lib as pl
import parse_relations as pr
from table_utils import table_to_dict

COLUMN_TITLES = ['tag', 'name', 'keyword', 'valueRepresentation', 'valueMultiplicity', 'retired']
ATTR_TABLE_ID = 'table_6-1'

def get_attribute_table(standard):
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_table_div(all_tables, ATTR_TABLE_ID)
    list_table = attribute_table_to_list(html_table)
    return table_to_dict(list_table, COLUMN_TITLES)

def attribute_table_to_list(table_div):
    '''
    Unlike other extract steps, attributes do not have a processing
    stage. Therefore, the HTML does not have to be preserved and the
    text can be directly parsed with `cell.text.strip()`.
    '''
    return [[cell.text.strip() for cell in row.find_all('td')]
            for row in pr.table_rows(table_div)]


def table_to_json(table):
    attribute_dict = {}
    for attr in table:
        attr_slug = pl.create_slug(attr['tag'])
        attribute_dict[attr_slug] = attr
        attribute_dict[attr_slug]['tag'] = attr['tag'].upper()
        attribute_dict[attr_slug]['retired'] = False if attr['retired'] == '' else True
    return attribute_dict


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table = get_attribute_table(standard)
    parsed_table_data = table_to_json(table)
    pl.write_pretty_json(sys.argv[2], parsed_table_data)
