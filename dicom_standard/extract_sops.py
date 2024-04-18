from typing import List
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.table_utils import TableDictType, get_table_rows_from_ids

COLUMN_TITLES = ['name', 'id', 'ciod']
TABLE_IDS = ['table_B.5-1', 'table_I.4-1', 'table_GG.3-1']


def generate_ciod_id(name: str) -> str:
    cleaned_name = name.split('IOD')[0].strip()
    # Standard workaround: Table B.5-1 is missing part of the IOD name ("Confocal Microscopy Tiled Pyramidal" instead of "Confocal Microscopy Tiled Pyramidal Image")
    # https://dicom.nema.org/medical/dicom/current/output/chtml/part04/sect_B.5.html#table_B.5-1
    if cleaned_name == 'Confocal Microscopy Tiled Pyramidal':
        cleaned_name = 'Confocal Microscopy Tiled Pyramidal Image'
    # Standard workaround: Table B.5-1 has a miscapitalized word in an IOD Specification
    # https://dicom.nema.org/medical/dicom/current/output/chtml/part04/sect_B.5.html#table_B.5-1
    if cleaned_name == 'Pseudo-color Softcopy Presentation State':
        cleaned_name = 'Pseudo-Color Softcopy Presentation State'
    return cleaned_name


def sop_table_to_json(table: List[TableDictType]) -> List[TableDictType]:
    sops = []
    for sop in table:
        sop['ciod'] = generate_ciod_id(sop['ciod'])
        sops.append(sop)
    return sops


if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    table = get_table_rows_from_ids(standard, TABLE_IDS, COLUMN_TITLES)
    parsed_table_data = sop_table_to_json(table)
    pl.write_pretty_json(parsed_table_data)
