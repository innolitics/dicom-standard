'''
modules_attributes.py

Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''

import json
import pickle
import re
import sys

from bs4 import BeautifulSoup

import parse_lib as pl

def get_module_attr_raw(standard_path, json_path):
    standard_file = open(standard_path, 'r')
    standard = BeautifulSoup(standard_file, 'html.parser')

    module_table_pattern = re.compile(".*Module Attributes$")
    basic_entry_header_pattern = re.compile(".*BASIC CODED ENTRY ATTRIBUTES$")
    enhanced_encoding_header_pattern = re.compile(".*ENHANCED ENCODING MODE$")
    link_pattern = re.compile(".*Include.*")

    all_tables = standard.find_all('div', class_='table')
    module_table_divs = pl.get_chapter_table_divs(standard, 'chapter_C')
    module_attr_rough = open(json_path, 'w')
    for tdiv in module_table_divs:
        data = []
        table_name = tdiv.p.strong.get_text()
        if (module_table_pattern.match(table_name)):
            table_body = tdiv.div.table.tbody
            table = pl.table_to_list(tdiv, all_tables)
            table = pl.expand_spans(table)
            attr_names = [row[0] for row in table]
            attr_tags = [row[1] for row in table]
            attr_types = [row[2] for row in table]
            attr_descriptions = [row[3] for row in table]
            json_list = [table_name]
            for i in range (len(attr_descriptions)):
                json_list.append({'Attribute:': attr_names[i], 'Tag': attr_tags[i], 'Type': attr_types[i], 'Description': attr_descriptions[i]});
            module_attr_rough.write(json.dumps(json_list, sort_keys=True, indent=4, separators=(',',':')) + "\n")
    module_attr_rough.close()

if __name__ == '__main__':
    try:
        get_module_attr_raw(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
