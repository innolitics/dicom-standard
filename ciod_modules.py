'''
ciod_modules.py

Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
Output the tables in JSON format, one entry per module.
'''
import sys
import re

import parse.parse_lib as pl

def main(standard_path, json_path):
    standard = pl.get_bs_from_html(standard_path)
    ciod_json_list = pl.get_table_data_from_standard(standard, 'ciods')
    descriptions = get_ciod_descriptions_from_standard(standard)
    final_json_list = add_ciod_description_fields(ciod_json_list, descriptions)
    pl.dump_pretty_json(json_path, 'w', final_json_list)

def add_ciod_description_fields(ciod_json_list, descriptions):
    i = 0
    for ciod in ciod_json_list:
        ciod['description'] = descriptions[i]
        i += 1
    return ciod_json_list

def get_ciod_descriptions_from_standard(standard):
    filtered_tables = find_ciod_tables(standard)
    descriptions = []
    for tdiv in filtered_tables:
        descriptions.append(find_description_text_in_html(tdiv))
    return descriptions

def find_ciod_tables(standard):
    match_pattern = re.compile(".*IOD Modules$")
    chapter_tables = pl.get_all_tdivs_from_chapter(standard, 'chapter_A')
    filtered_tables = [table for table in chapter_tables
                       if match_pattern.match(table.p.strong.get_text())]
    return filtered_tables

def find_description_text_in_html(tdiv):
    section = tdiv.parent.parent
    description_title = section.find('h3', class_='title')
    try:
        description_text = description_title.parent.parent.parent.parent.p.get_text()
        return description_text
    except AttributeError:
        return None

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
