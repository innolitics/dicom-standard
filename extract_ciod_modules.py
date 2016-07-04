'''
Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
Output the tables in JSON format, one entry per module.
'''
import sys
import re

import parse_lib as pl

def ciod_module_data_from_standard(standard):
    chapter_name = "chapter_A"
    match_pattern = re.compile(".*IOD Modules$")
    column_titles = ['information_entity', 'module', 'link_to_standard', 'usage']
    column_correction = False
    return table_data_from_standard(standard, chapter_name, match_pattern,
                                    column_titles, column_correction)


def expand_module_usage_fields(ciod_json_raw):
    for ciod in ciod_json_raw:
        for module in ciod['data']:
            usage, conditional_statement = expand_conditional_statement(module['usage'])
            module['usage'] = usage
            module['conditional_statement'] = conditional_statement

def expand_conditional_statement(usage_field):
    conditional = re.compile("^C.*")
    if conditional.match(usage_field):
        usage, *conditional_statement_parts = re.split("-", usage_field)
        conditional_statement = ''.join(conditional_statement_parts).strip()
    else:
        usage = usage_field
        conditional_statement = None
    return usage.strip(), conditional_statement

def add_ciod_description_fields(ciod_json_list, descriptions):
    i = 0
    for ciod in ciod_json_list:
        ciod['description'] = descriptions[i]
        i += 1
    return ciod_json_list

def ciod_descriptions_from_standard(standard):
    filtered_tables = find_ciod_tables(standard)
    descriptions = list(map(find_description_text_in_html, filtered_tables))
    return descriptions

def find_ciod_tables(standard):
    match_pattern = re.compile(".*IOD Modules$")
    chapter_tables = pl.all_tdivs_in_chapter(standard, 'chapter_A')
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
    standard = pl.parse_html_file(sys.argv[1])
    ciod_json_list = ciod_module_data_from_standard(standard)
    expand_module_usage_fields(ciod_json_list)
    descriptions = ciod_descriptions_from_standard(standard)
    final_json_list = add_ciod_description_fields(ciod_json_list, descriptions)
    pl.dump_pretty_json(sys.argv[2], 'w', final_json_list)
