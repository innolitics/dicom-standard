'''
modules_attributes.py

Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''

import json
import re
import sys

from bs4 import BeautifulSoup

import parse_lib as pl

def get_module_attr_raw(standard_path, json_path):
    with open(standard_path, 'r') as standard_file, open(json_path, 'w') as module_attr_rough:
        standard = BeautifulSoup(standard_file, 'html.parser')
        module_table_pattern = re.compile(".*Module Attributes$")

        all_tables = standard.find_all('div', class_='table')
        module_table_divs = pl.get_chapter_table_divs(standard, 'chapter_C')
        for tdiv in module_table_divs:
            table_name = tdiv.p.strong.get_text()
            if (module_table_pattern.match(table_name)):
                table_body = tdiv.div.table.tbody
                raw_table = pl.table_to_list(tdiv, all_tables)
                expanded_table = pl.expand_spans(raw_table)
                full_table = correct_for_missing_type_column(expanded_table)
                attr_names, attr_tags, attr_types, attr_descriptions = zip(*full_table)
                table_data = []
                for a_name, a_tag, a_type, a_descr in zip(attr_names, attr_tags, attr_types, attr_descriptions):
                    table_data.append({'Attribute:': a_name, 'Tag': a_tag, 'Type': a_type, 'Description': a_descr});
                json_list = [{
                    'tableName': table_name,
                    'tableData': table_data
                }]
                module_attr_rough.write(json.dumps(json_list, sort_keys=False, indent=4, separators=(',',':')) + "\n")

def correct_for_missing_type_column(full_table):
    corrected_table = []
    for a_name, a_tag, a_type, a_descr in full_table:
        corrected_row = [a_name, a_tag]
        if a_descr is None:
            a_corrected_type = a_descr
            a_corrected_descr = a_type
            corrected_row.extend([a_corrected_type, a_corrected_descr])
        else:
            corrected_row.extend([a_type, a_descr])
        corrected_table.append(corrected_row)
    return corrected_table

if __name__ == '__main__':
    try:
        get_module_attr_raw(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
