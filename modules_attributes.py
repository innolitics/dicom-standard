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
    # standard = None
    # with open(standard_path, 'rb') as standard_file:
        # standard = pickle.load(standard_file)
    '''
    THIS IS INEFFICIENT. 
    1. Code above uses pickle to pass the parsable object between files. It doesn't work,
        the file is too big and pickle will either segfault or have a recursive timeout.
    2. Code blow simply recreates the beautifulsoup object, which is very time consuming.
    '''
    standard_file = open(standard_path, 'r')
    standard = BeautifulSoup(standard_file, 'html.parser')

    module_table_pattern = re.compile(".*Module Attributes$")
    basic_entry_header_pattern = re.compile(".*BASIC CODED ENTRY ATTRIBUTES$")
    enhanced_encoding_header_pattern = re.compile(".*ENHANCED ENCODING MODE$")
    link_pattern = re.compile(".*Include.*")
    all_tables = standard.find_all('div', class_='table')
    module_table_divs = pl.get_chapter_table_divs(standard, 'chapter_C')
    module_attr_rough = open(json_path, 'w')
    # Extract all the module description tables
    for tdiv in module_table_divs:
        data = []
        table_name = tdiv.p.strong.get_text()
        if (module_table_pattern.match(table_name)):
            table_body = tdiv.div.table.tbody
            table_fields = pl.separate_table_data(table_body,['names', 'tags', 'types', 'descriptions'], standard, follow_links=True)
            attr_names = table_fields[0]
            attr_tags = table_fields[1] 
            attr_types = table_fields[2] 
            attr_descriptions = table_fields[3] 
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
