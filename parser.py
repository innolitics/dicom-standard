# parser.py
#
# Parse the DICOM standard HTML file to extract the composite
# IOD table, module table, attributes table, and their 
# relationship tables.

from bs4 import BeautifulSoup
import json
import subprocess as sp

def main():
    # Modify incoming html file to remove illegal unicode characters
    # TODO: this will later be moved to a Makefile macro
    sp.call(['cp', './PS3.3.html', './temp_standard.html'])
    sp.call(['sed', '-i', '-e', "s/&nbsp;/ /g", './temp_standard.html'])

    html_doc = open('./temp_standard.html', 'r')
    standard = BeautifulSoup(html_doc, 'html.parser')

    ciod_table_divs = get_composite_IOD_divs(standard)
    # Extract all the composite IOD tables 
    for tdiv in ciod_table_divs:
        data = []
        table_body = tdiv.div.table.tbody
        table_name = tdiv.p.strong.get_text()
        table_data = extract_table_data(table_body)
        print(table_name)
        print(table_data)
        # Below is the json encoding for tables A.2-1 and on
        # TODO: divide the chapter A tables up into groups
        # json.dumps([table_name, {'IE': unicode(table_data[0]),'Module': unicode(table_data[1]), 'Reference': unicode(table_data[2]), 'Usage': unicode(table_data[3])} ])

def extract_table_data(table_body):
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data

def get_composite_IOD_divs(standard):
    table_divs = []
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if (chapter.div.div.div.h1.a.get('id') == 'chapter_A'):
            table_divs = chapter.find_all('div', class_='table')
            return table_divs

main()
