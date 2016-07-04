'''
Read the table from PS3.6 to determine the value multiplicity and value
representation of the different DICOM attributes. Output this information in a
JSON file, which will then be appended to the attribute list from PS3.3.
'''
import sys
import json
import re

from bs4 import BeautifulSoup

import parse_lib as pl

def find_attribute_properties(standard):
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_table_div(all_tables, 'table_6-1')
    table_data = extract_table_data(html_table.div.table.tbody)
    properties_dict = properties_to_dict(table_data)
    return properties_dict

def properties_to_dict(table_data):
    properties_dict = {}
    for tag, name, keyword, value_representation, value_multiplicity, extra in table_data:
        if extra is not None:
            retired = re.match("RET", extra) is not None
        else:
            retired = False
        properties_dict[tag] = {
            "keyword": keyword,
            "value_representation": value_representation,
            "value_multiplicity": value_multiplicity,
            "name": name,
            "retired": retired
        }
    return properties_dict

def extract_table_data(table_body):
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    return data

def main(standard_path, json_path):
    standard = pl.parse_html_file(standard_path)
    table_data = find_attribute_properties(standard)
    pl.dump_pretty_json(json_path, 'w', table_data)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
