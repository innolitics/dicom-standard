'''
vr_vm_attributes.py
Read the table from PS3.6 to determine the value multiplicity and value
representation of the different DICOM attributes. Output this information in a
JSON file, which will then be appended to the attribute list from PS3.3. 
'''
import sys
import json

from bs4 import BeautifulSoup

import parse_lib as pl

def get_data_characteristic_attributes(standard):
    all_tables = standard.find_all('div', class_='table')
    html_table = pl.find_table_div(all_tables, 'table_6-1')
    raw_table_data = extract_table_data(html_table.div.table.tbody)
    table_data = remove_irregular_rows(raw_table_data)
    json_data = {}
    for tag, name, keyword, vr, *vm in table_data:
        retired = len(vm) > 1
        json_data[tag] = { 
                           "keyword": keyword,
                           "vr": vr,
                           "vm": vm[0],
                           "retired": retired
                           }
    return json_data 

def remove_irregular_rows(table):
    new_table = [row for row in table if len(row) >= 5]
    return new_table

def extract_table_data(table_body):
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    return data
        
def main(standard_path, json_path):
    standard = pl.get_bs_from_html(standard_path)
    table_data = get_data_characteristic_attributes(standard) 
    pl.dump_pretty_json(json_path, 'w', table_data)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
