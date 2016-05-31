# parser.py
#
# Parse the DICOM standard HTML file to extract the composite
# IOD table, module table, attributes table, and their 
# relationship tables.

from bs4 import BeautifulSoup
import json
import re

def main():
    html_doc = open('temp_standard.html', 'r')
    standard = BeautifulSoup(html_doc, 'html.parser')
    
    iod_table_pattern = re.compile(".*IOD Modules$")

    ciod_table_divs = get_composite_IOD_divs(standard)
    # Extract all the composite IOD tables 
    for tdiv in ciod_table_divs:
        data = []
        table_name = tdiv.p.strong.get_text()
        if iod_table_pattern.match(table_name):
            table_body = tdiv.div.table.tbody
            table_data = extract_table_data(table_body)
            last_ie = table_data[0][0]
            ies = []
            modules = []
            references = []
            usage = []
            for row in table_data:
                try: 
                    i = 0
                    # If row has three entries, it's because the first column is merged. Use
                    # the previous IE entry to get the correct value here.
                    if (len(row) < 4):
                        ies.append(last_ie)
                        i = 0
                    else:
                        ies.append(row[0])
                        last_ie = row[0]
                        i = 1
                    modules.append(row[i])
                    i += 1
                    references.append(row[i])
                    i += 1
                    usage.append(row[i])
                except IndexError:
                    print("Index error, table row not conforming to standard IOD table structure.")
            print json.dumps([table_name, {'IE': unicode(ies),'Module': unicode(modules), 'Reference': unicode(references), 'Usage': unicode(usage)} ], sort_keys=True, indent=4, separators=(',',':'))
            
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
