from typing import Tuple, List
import re
import sys

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.extract_attributes import attribute_table_to_list
from dicom_standard.table_utils import AttributeDictType, table_to_dict

COLUMN_TITLES = ['name', 'id', 'iod']
TABLE_ID = 'table_B.5-1'
IOD_ABBREVIATIONS = {
    'computed radiography': 'cr',
    'computed tomography': 'ct',
    'magnetic resonance': 'mr',
    'nuclear medicine': 'nm',
    'ultrasound': 'us',
    'secondary capture': 'sc',
    'x-ray radiofluoroscopic': 'xrf',
    'radiotherapy': 'rt',
    'positron emission tomography': 'pet',
    'electrocardiogram': 'ecg',
    'electrophysiology': 'ep',
    'oct': 'oct image',
    'enhanced x-ray rf image': 'enhanced xrf image',
    'x-ray rf': 'xrf',
}
ID_PATTERN = re.compile(r'\b(' + '|'.join(IOD_ABBREVIATIONS.keys()) + r')\b')


def get_table_and_tdiv(standard: BeautifulSoup) -> Tuple[List[AttributeDictType], Tag]:
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_tdiv_by_id(all_tables, TABLE_ID)
    list_table = attribute_table_to_list(html_table)
    table_dict_list = table_to_dict(list_table, COLUMN_TITLES)
    return (table_dict_list, html_table)


def generate_ciod_id(name: str) -> str:
    cleaned_name = name.split('Storage')[0].strip()
    return ID_PATTERN.sub(lambda x: IOD_ABBREVIATIONS[x.group()], cleaned_name.lower())


def table_to_json(table: List[AttributeDictType], tdiv: Tag) -> List[AttributeDictType]:
    attributes = []
    for row in table:
        ciodId = pl.create_slug(generate_ciod_id(row['name']))
        row['ciodId'] = ciodId
        row.pop('iod', None)
        attributes.append(row)
    return attributes


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table, tdiv = get_table_and_tdiv(standard)
    parsed_table_data = table_to_json(table, tdiv)
    pl.write_pretty_json(parsed_table_data)
