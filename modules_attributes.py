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
            table_data = pl.extract_table_data(table_body)
            attr_names = []
            attr_tags = []
            attr_types = []
            attr_descriptions = []
            ref_links = pl.get_include_links(table_body)
            i = 0
            for row in table_data:
                try:
                    # There seem to be only two headers like this in the whole standard. They break form, so 
                    # we catch them with a regex match.
                    if (basic_entry_header_pattern.match(row[0]) or enhanced_encoding_header_pattern.match(row[0])):
                        i += 1
                        continue
                    if (ref_links[i] is not None):
                        a_name, a_tag, a_type, a_descrip = get_linked_attrs(all_tables, ref_links[i])
                        attr_names.extend(a_name)
                        attr_tags.extend(a_tag)
                        attr_types.extend(a_type)
                        attr_descriptions.extend(a_descrip)
                        i += 1
                        continue
                    else:
                        attr_names.append(row[0])
                    attr_tags.append(row[1])
                    j = 2
                    if (len(row) < 4):
                        attr_types.append(None)     
                    else:
                        attr_types.append(row[j])
                        j += 1
                    attr_descriptions.append(row[j])
                except IndexError:
                    module_attr_rough.write("Index error, table row not conforming to standard module-attribute structure.\n")
                    # Catch errors and insert None into each field as a placeholder.
                    if (len(attr_names)-1 == i):
                        attr_names[len(attr_names)-1] = None
                    else:
                        attr_names.append(None)
                    if (len(attr_tags)-1 == i):
                        attr_tags[len(attr_tags)-1] = None
                    else:
                        attr_tags.append(None)
                    if (len(attr_types)-1 == i):
                        attr_types[len(attr_types)-1] = None
                    else:
                        attr_types.append(None)
                    if (len(attr_descriptions)-1 == i):
                        attr_descriptions[len(attr_descriptions)-1] = None
                    else:
                        attr_descriptions.append(None)
                i += 1

            json_list = [table_name]
            for i in range (len(attr_descriptions)):
                json_list.append({'Attribute:': attr_names[i], 'Tag': attr_tags[i], 'Type': attr_types[i], 'Description': attr_descriptions[i]});
            module_attr_rough.write(json.dumps(json_list, sort_keys=True, indent=4, separators=(',',':')) + "\n")
    module_attr_rough.close()

def get_linked_attrs(all_tables, ref_id):
    basic_entry_header_pattern = re.compile(".*BASIC CODED ENTRY ATTRIBUTES$")
    enhanced_encoding_header_pattern = re.compile(".*ENHANCED ENCODING MODE$")
    attr_names = []
    attr_tags = []
    attr_types = []
    attr_descriptions = []
    for table in all_tables:
        if (table.a.get('id') == ref_id):
            table_body = table.div.table.tbody
            table_data = pl.extract_table_data(table_body)
            ref_links = pl.get_include_links(table_body)
            # Prevent an infinitely recursive reference
            for i in range(len(ref_links)):
                if (ref_links[i] == ref_id):
                    ref_links[i] = None
            i = 0
            for row in table_data:
                # There seem to be only two headers like this in the whole standard. They break form, so 
                # we catch them with a specific regex match.
                if (basic_entry_header_pattern.match(row[0]) or enhanced_encoding_header_pattern.match(row[0])):
                    i += 1
                    continue
                if (ref_links[i] is not None):
                    a_name, a_tag, a_type, a_descrip = get_linked_attrs(all_tables, ref_links[i])
                    attr_names.extend(a_name)
                    attr_tags.extend(a_tag)
                    attr_types.extend(a_type)
                    attr_descriptions.extend(a_descrip)
                    i += 1
                    continue
                else:
                    attr_names.append(row[0])
                attr_tags.append(row[1])
                j = 2
                if (len(row) < 4):
                    attr_types.append(None)     
                else:
                    attr_types.append(row[j])
                    j += 1
                attr_descriptions.append(row[j])
                i += 1
    return (attr_names, attr_tags, attr_types, attr_descriptions) 

if __name__ == '__main__':
    try:
        get_module_attr_raw(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
