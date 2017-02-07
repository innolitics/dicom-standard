'''
Load the module-attribute tables from DICOM Standard PS3.3, Annex C.
Expand out macros in-line for each module. Output the tables in JSON
format, one entry per attribute.
'''
import sys
import re

import parse_lib as pl
import parse_relations as pr
from table_utils import expand_spans, table_to_dict, stringify_table, tdiv_to_table_list

MODULE_CHAPTER_ID = 'chapter_C'
MODULE_TABLE_SUFFIX = re.compile("(.*Module Attributes$)|(.*Module Table$)")
MODULE_COLUMN_TITLES = ['name', 'tag', 'type', 'description', 'macro_table_id']

URL_PREFIX = "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#"

def module_attribute_data_from_standard(standard):
    chapter_name = "chapter_C"
    match_pattern = re.compile("(.*Module Attributes$)|(.*Module Table$)")
    column_titles = ['name', 'tag', 'type', 'description', 'macro_table_id']
    column_correction = True
    return pl.table_data_from_standard(standard, chapter_name, match_pattern,
                                    column_titles, column_correction)

def get_module_tables(standard):
    chapter_C_table_divs = pl.all_tdivs_in_chapter(standard, MODULE_CHAPTER_ID)
    module_table_divs = list(filter(is_valid_module_table, chapter_C_table_divs))
    module_table_lists = list(map(tdiv_to_table_list, module_table_divs))
    return (module_table_lists, module_table_divs)

def is_valid_module_table(table_div):
    return MODULE_TABLE_SUFFIX.match(pr.table_name(table_div))


def tables_to_json(tables, tdivs):
    expanded_tables = list(map(expand_spans, tables))
    stringified_tables = map(stringify_table, expanded_tables)
    table_dicts = map(module_table_to_dict, stringified_tables)
    return list(map(get_table_with_metadata, zip(table_dicts, tdivs)))

def module_table_to_dict(table):
    return table_to_dict(table, MODULE_COLUMN_TITLES)

def get_table_with_metadata(table_with_tdiv):
    table, tdiv = table_with_tdiv
    clean_name = pl.clean_table_name(pr.table_name(tdiv))
    return {
            'name': clean_name,
            'attributes': table, # TODO: Update refactor proposal for this.
            'id': pl.create_slug(clean_name),
            'description': str(pr.table_description(tdiv)),
            'linkToStandard': URL_PREFIX + pr.table_id(tdiv)
    }

if __name__ == '__main__':
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_module_tables(standard)
    parsed_table_data = tables_to_json(tables, tdivs)
    pl.write_pretty_json(sys.argv[2], parsed_table_data)
