from typing import List
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.table_utils import TableDictType, get_table_rows_from_ids

COLUMN_TITLES = ['name', 'id', 'ciod']
TABLE_IDS = ['table_B.5-1', 'table_I.4-1', 'table_GG.3-1']
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


def generate_ciod_id(name: str) -> str:
    cleaned_name = name.split('IOD')[0].strip()
    return IOD_ABBREVIATIONS.get(cleaned_name, cleaned_name)


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
