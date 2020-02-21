'''
Extract the listing of all attributes given in PS3.6 of the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.table_utils import table_to_dict

COLUMN_TITLES = ['tag', 'name', 'keyword', 'valueRepresentation', 'valueMultiplicity', 'retired']
ATTR_TABLE_IDS = ['table_6-1', 'table_7-1', 'table_8-1', 'table_9-1']

def get_attribute_table(standard):
    attr_dict_list = []
    all_tables = standard.find_all('div', class_='table')
    for table_id in ATTR_TABLE_IDS:
        html_table = pl.find_tdiv_by_id(all_tables, table_id)
        list_table = attribute_table_to_list(html_table)
        table_dict_list = table_to_dict(list_table, COLUMN_TITLES)
        attr_dict_list.extend(table_dict_list)
    return attr_dict_list


def attribute_table_to_list(table_div):
    return [[cell.text.strip() for cell in row.find_all('td')]
            for row in pr.table_rows(table_div)]


def attribute_table_to_json(table):
    attribute_dict = {}
    for attr in table:
        attr_slug = pl.create_slug(attr['tag'])
        attribute_dict[attr_slug] = attr
        attribute_dict[attr_slug]['tag'] = attr['tag'].upper()
        attribute_dict[attr_slug]['retired'] = True if attr['retired'] == 'RET' else False
    return attribute_dict


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table = get_attribute_table(standard)
    parsed_table_data = attribute_table_to_json(table)
    pl.write_pretty_json(parsed_table_data)
