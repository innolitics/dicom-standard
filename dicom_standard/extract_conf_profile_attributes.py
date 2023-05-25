'''
Extract the listing of all attributes given in table E.1-1 from part 15 of the DICOM Standard.
'''
from typing import cast, Dict, List, Union
import sys

from bs4 import BeautifulSoup

from dicom_standard import parse_lib as pl
from dicom_standard.table_utils import TableDictType, table_to_list, table_to_dict

COLUMN_TITLES = [
    'name', 'tag', 'retired', 'stdCompIOD', 'basicProfile', 'rtnSafePrivOpt',
    'rtnUIDsOpt', 'rtnDevIdOpt', 'rtnInstIdOpt', 'rtnPatCharsOpt', 'rtnLongFullDatesOpt',
    'rtnLongModifDatesOpt', 'cleanDescOpt', 'cleanStructContOpt', 'cleanGraphOpt',
]
TABLE_ID = 'table_E.1-1'

AttrTableType = List[Dict[str, Union[str, bool]]]

def ignore_retirement_mismatch(attr_name: str) -> bool:
    if attr_name in [ 'Time of Document or Verbal Transaction (Trial)']:
        return True
    return False

def get_conf_profile_table(standard: BeautifulSoup) -> List[TableDictType]:
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_tdiv_by_id(all_tables, TABLE_ID)
    list_table = table_to_list(html_table)
    return table_to_dict(list_table, COLUMN_TITLES, omit_empty=True)


def table_to_json(table: List[TableDictType]) -> List[TableDictType]:
    attributes = []
    for attr in table:
        attr['id'] = pl.create_slug(attr['tag'])
        attr['tag'] = attr['tag'].upper()
        attributes.append(attr)
    return attributes


def verify_table_integrity(parsed_table_data: List[TableDictType], attributes: AttrTableType):
    retired_attrs = [d['name'] for d in attributes if d['retired'] == 'Y']
    errors = []
    for attr in parsed_table_data:
        attr_name = attr['name']
        retired = attr['retired'] == 'Y'
        if retired and attr['name'] not in retired_attrs and not ignore_retirement_mismatch(attr_name):
            errors.append(f'Attribute "{attr_name}" {attr["tag"]} is retired in Table '
                          'E.1-1 but not in Table 6-1.')
        if not retired and attr['name'] in retired_attrs and not ignore_retirement_mismatch(attr_name):
            errors.append(f'Attribute "{attr_name}" {attr["tag"]} is retired in Table '
                          '6-1 but not in Table E.1-1.')
    if errors:
        errors.insert(0, 'One or more attributes in tables 6-1 and E.1-1 have inconsistent properties between tables:')
        error_msg = '\n'.join(errors)
        raise Exception(error_msg)


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    attributes = pl.read_json_data(sys.argv[2])
    table = get_conf_profile_table(standard)
    parsed_table_data = table_to_json(table)
    verify_table_integrity(parsed_table_data, cast(AttrTableType, attributes))
    for attr in parsed_table_data:
        del attr['retired']
    pl.write_pretty_json(parsed_table_data)
