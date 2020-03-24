'''
Takes the extracted CIOD-Macro table information to build a list of all
CIOD-Macro relationships defined in the DICOM Standard.
'''
import sys

from dicom_standard import parse_lib as pl

from process_ciod_module_relationship import expand_conditional_statement
                                              

def define_all_relationships(ciod_macro_list):
    all_relationships = []
    for table in ciod_macro_list:
        ciod = table['name']
        macros = table['macros']
        all_relationships.extend([define_ciod_macro_relationship(ciod, macro)
                                  for macro in macros])
    return all_relationships


def define_ciod_macro_relationship(ciod, macro):
    usage, conditional_statement = expand_conditional_statement(macro['usage'])
    return {
        "ciodId": pl.create_slug(ciod),
        "macroId": pl.create_slug(pl.text_from_html_string(macro['macro'])),
        "usage": usage,
        "conditionalStatement": conditional_statement
    }


if __name__ == '__main__':
    ciod_macro_list = pl.read_json_to_dict(sys.argv[1])
    ciod_macro_relationships = define_all_relationships(ciod_macro_list)
    pl.write_pretty_json(ciod_macro_relationships)
