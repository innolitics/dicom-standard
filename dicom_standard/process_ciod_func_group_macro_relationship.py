'''
Takes the extracted CIOD-Functional Group Macro table information to build a list of all
CIOD-Functional Group Macro relationships defined in the DICOM Standard.
'''
import re
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.process_ciod_module_relationship import expand_conditional_statement


# Standard workaround: Remove "Macro" from "Frame VOI LUT With LUT Macro" in Table A.84.3.2-1
# http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.84.3.2.html#table_A.84.3.2-1
# Standard workaround: Remove "Macro Attributes" from "Photoacoustic Reconstruction Algorithm Macro Attributes" in Table A.89.4-1
# https://dicom.nema.org/medical/dicom/2023c/output/html/part03.html#table_A.89.4-1
def clean_macro_name(text):
    return re.sub(' Macro', '', re.sub(' Macro Attributes','',text)).strip()


def define_all_relationships(ciod_macro_list):
    all_relationships = []
    for table in ciod_macro_list:
        ciod = table['name']
        macros = table['macros']
        module_type = table['moduleType']
        all_relationships.extend([define_ciod_macro_relationship(ciod, macro, module_type)
                                  for macro in macros])
    return all_relationships


def define_ciod_macro_relationship(ciod, macro, module_type):
    usage, conditional_statement = expand_conditional_statement(macro['usage'])
    return {
        "ciodId": pl.create_slug(ciod),
        "macroId": pl.create_slug(clean_macro_name(pl.text_from_html_string(macro['macro']))),
        "usage": usage,
        "conditionalStatement": conditional_statement,
        "moduleType": module_type,
    }


if __name__ == '__main__':
    ciod_macro_list = pl.read_json_data(sys.argv[1])
    ciod_macro_relationships = define_all_relationships(ciod_macro_list)
    pl.write_pretty_json(ciod_macro_relationships)
