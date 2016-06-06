'''
ciod_modules.py

Load the CIOD module tables from DICOM Standard PS3.3, Annex A.
Output the tables in JSON format, one entry per module.
'''
import json
import re
import sys

from bs4 import BeautifulSoup

import parse_lib as pl

def get_ciod_module_raw(standard_path, json_path):
    with open(standard_path, 'r') as standard_file, open(json_path, 'w') as ciod_module_rough:
        standard = BeautifulSoup(standard_file, 'html.parser')
        iod_table_pattern = re.compile(".*IOD Modules$")

        ciod_table_divs = pl.get_chapter_table_divs(standard, 'chapter_A')
        all_tables = standard.find_all('div', class_='table')
        for tdiv in ciod_table_divs:
            table_name = tdiv.p.strong.get_text()
            if iod_table_pattern.match(table_name):
                table_body = tdiv.div.table.tbody
                urls = pl.extract_doc_links(table_body)
                raw_table = pl.table_to_list(tdiv, all_tables)
                full_table = pl.expand_spans(raw_table)
                ies, modules, references, usage = zip(*full_table)
                table_data = []
                for ie, module, ref, use, url in zip(ies, modules, references, usage, urls):
                    table_data.append({'IE Name': ie, 'Module': module, 'Doc Reference': ref, 'Usage': use, 'URL': url})
                json_list = [{
                    'tableName': table_name,
                    'tableData': table_data
                }]
                ciod_module_rough.write(json.dumps(json_list, sort_keys=False, indent=4, separators=(',',':')) + "\n")

if __name__ == '__main__':
    try:
        get_ciod_module_raw(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON object.")
