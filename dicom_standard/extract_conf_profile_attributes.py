'''
Extract the listing of all attributes given in table E.1-1 from part 15 of the DICOM Standard.
'''
from typing import List, Dict
import sys

from bs4 import BeautifulSoup

from dicom_standard import parse_lib as pl
from dicom_standard.extract_attributes import attribute_table_to_list
from dicom_standard.table_utils import AttributeDictType, table_to_dict

COLUMN_TITLES = [
    'attributeName', 'tag', 'retired', 'stdCompIOD', 'basicProfile', 'rtnSafePrivOpt',
    'rtnUIDsOpt', 'rtnDevIdOpt', 'rtnInstIdOpt', 'rtnPatCharsOpt', 'rtnLongFullDatesOpt',
    'rtnLongModifDatesOpt', 'cleanDescOpt', 'cleanStructContOpt', 'cleanGraphOpt',
]
TABLE_ID = 'table_E.1-1'


def get_conf_profile_table(standard: BeautifulSoup) -> List[AttributeDictType]:
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_tdiv_by_id(all_tables, TABLE_ID)
    list_table = attribute_table_to_list(html_table)
    return table_to_dict(list_table, COLUMN_TITLES, omit_empty=True)


def table_to_json(table: List[AttributeDictType]) -> Dict[str, AttributeDictType]:
    attribute_dict = {}
    for attr in table:
        attr_slug = pl.create_slug(attr['tag'])
        attribute_dict[attr_slug] = attr
        attribute_dict[attr_slug]['tag'] = attr['tag'].upper()
    return attribute_dict


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table = get_conf_profile_table(standard)
    parsed_table_data = table_to_json(table)
    pl.write_pretty_json(parsed_table_data)
