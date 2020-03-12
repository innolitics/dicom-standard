from typing import Tuple, List
import re
import sys

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard.extract_attributes import attribute_table_to_list
from dicom_standard.table_utils import AttributeDictType, table_to_dict

COLUMN_TITLES = ['name', 'id', 'iod']
TABLE_ID = 'table_B.5-1'
IOD_ABBREVIATIONS = {
    'Computed Radiography': 'CR',
    'Computed Tomography': 'CT',
    'Magnetic Resonance': 'MR',
    'Nuclear Medicine': 'NM',
    'Ultrasound': 'US',
    'Secondary Capture': 'SC',
    'Radiotherapy': 'RT',
    'Positron Emission Tomography': 'PET',
    'Electrocardiogram': 'ECG',
    'Electrophysiology': 'EP',
    'OCT': 'OCT Image',
    'Enhanced X-Ray RF Image': 'Enhanced XRF Image',
    'X-Ray Radiofluoroscopic': 'XRF',
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
    return cleaned_name


def table_to_json(table: List[AttributeDictType], tdiv: Tag) -> List[AttributeDictType]:
    attributes = []
    for row in table:
        ciod = generate_ciod_id(row['name'])
        row['ciod'] = ciod
        row.pop('iod', None)
        attributes.append(row)
    return attributes


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table, tdiv = get_table_and_tdiv(standard)
    parsed_table_data = table_to_json(table, tdiv)
    pl.write_pretty_json(parsed_table_data)
