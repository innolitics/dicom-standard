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

def get_vr_vm_attributes(standard_path, json_path):
    with open(standard_path, 'r') as standard_html, open(json_path, 'w') as json_file:
        standard = BeautifulSoup(standard_html, 'html.parser')
        all_tables = standard.find_all('div', class_='table')
        vr_vm_table = pl.find_table_div(all_tables, 'table_6-1')
        raw_vr_vm_data =extract_table_data(vr_vm_table.div.table.tbody);
        vr_vm_data = remove_irregular_rows(raw_vr_vm_data)
        table_data = []
        for tag, name, keyword, vr, *vm in vr_vm_data:
            table_data.append({ 
                               "Tag": tag,
                               "Keyword": keyword,
                               "VR": vr,
                               "VM": vm[0]
                             })
        json_dict = { "Table Data": table_data }
        json_file.write(json.dumps(json_dict, sort_keys=False, indent=4, separators=(',', ':')) + "\n")

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
         
if __name__ == '__main__':
    try:
        get_vr_vm_attributes(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the JSON file.")
