from typing import Tuple, List
import sys

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard.extract_attributes import attribute_table_to_list
from dicom_standard.table_utils import TableDictType, table_to_dict

COLUMN_TITLES = ['name', 'id', 'ciod']
TABLE_ID = 'table_B.5-1'
IOD_ABBREVIATIONS = {
    'Computed Radiography Image': 'CR Image',
    'Ultrasound Multi-frame Image': 'US Multi-frame Image',
    'Ultrasound Image': 'US Image',
    'Multi-frame Single Bit Secondary Capture Image': 'Multi-frame Single Bit SC Image',
    'Multi-frame Grayscale Byte Secondary Capture Image': 'Multi-frame Grayscale Byte SC Image',
    'Multi-frame Grayscale Word Secondary Capture Image': 'Multi-frame Grayscale Word SC Image',
    'Multi-frame True Color Secondary Capture Image': 'Multi-frame True Color SC Image',
    'Pseudo-color Softcopy Presentation State': 'Pseudo-Color Softcopy Presentation State',
    'Intravascular Optical Coherence Tomography': 'Intravascular Optical Coherence Tomography Image',  # Inconsistent name: http://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_A.66.html
    'Nuclear Medicine Image': 'NM Image',
    'Patient Radiation Dose SR': 'Patient Radiation Dose Structured Report',
    'Positron Emission Tomography Image': 'PET Image',
}


def get_table_and_tdiv(standard: BeautifulSoup) -> Tuple[List[TableDictType], Tag]:
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_tdiv_by_id(all_tables, TABLE_ID)
    list_table = attribute_table_to_list(html_table)
    table_dict_list = table_to_dict(list_table, COLUMN_TITLES)
    return (table_dict_list, html_table)


def generate_ciod_id(name: str) -> str:
    cleaned_name = name.split('IOD')[0].strip()
    return IOD_ABBREVIATIONS.get(cleaned_name, cleaned_name)


def table_to_json(table: List[TableDictType], tdiv: Tag) -> List[TableDictType]:
    attributes = []
    for row in table:
        row['ciod'] = generate_ciod_id(row['ciod'])
        attributes.append(row)
    return attributes


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table, tdiv = get_table_and_tdiv(standard)
    parsed_table_data = table_to_json(table, tdiv)
    pl.write_pretty_json(parsed_table_data)
