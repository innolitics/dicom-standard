from typing import Tuple, List
import sys

from bs4 import BeautifulSoup, Tag

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.extract_attributes import attribute_table_to_list
from dicom_standard.table_utils import AttributeDictType, table_to_dict

COLUMN_TITLES = ['name', 'UID', 'IODSpecification']
TABLE_ID = 'table_B.5-1'


def get_table_and_tdiv(standard: BeautifulSoup) -> Tuple[List[AttributeDictType], Tag]:
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_tdiv_by_id(all_tables, TABLE_ID)
    list_table = attribute_table_to_list(html_table)
    table_dict_list = table_to_dict(list_table, COLUMN_TITLES)
    return (table_dict_list, html_table)


def get_section_ids(tdiv: Tag) -> List[str]:
    return [
        f"{tag['href'].split('#')[-1]}.1"
        for row in pr.table_rows(tdiv)
        for tag in row.find_all('a', class_='olink')
    ]


def clean_ciod_name(name):
    return name.split('\xa0')[-1].replace(' IOD Description', '')


def get_ciod_ids(section_ids: List[str]) -> List[str]:
    standard = pl.parse_html_file(sys.argv[2])
    ciod_names = [standard.find(id=s_id).parent.text for s_id in section_ids]
    cleaned_names = list(map(clean_ciod_name, ciod_names))
    return list(map(pl.create_slug, cleaned_names))


def sop_table_to_json(table: List[AttributeDictType], tdiv: Tag) -> AttributeDictType:
    section_ids = get_section_ids(tdiv)
    ciod_ids = get_ciod_ids(section_ids)
    return {c_id: row['UID'] for c_id, row in zip(ciod_ids, table)}


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table, tdiv = get_table_and_tdiv(standard)
    parsed_table_data = sop_table_to_json(table, tdiv)
    pl.write_pretty_json(parsed_table_data)
