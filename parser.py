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
    get_ciod_module_raw(standard)
    get_module_attr_raw(standard)

def get_ciod_module_raw(standard):
    iod_table_pattern = re.compile(".*IOD Modules$")
    ciod_table_divs = get_chapter_table_divs(standard, 'chapter_A')
    # Extract all the composite IOD tables 
    ciod_module_rough = open('ciod_module_rough.json', 'w')
    for tdiv in ciod_table_divs:
        data = []
        table_name = tdiv.p.strong.get_text()
        if iod_table_pattern.match(table_name):
            table_body = tdiv.div.table.tbody
            table_data = extract_table_data(table_body)
            urls = extract_doc_links(table_body)
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
                    ciod_module_rough.write("Index error, table row not conforming to standard IOD table structure.\n")
            ciod_module_rough.write(json.dumps([table_name, {'IE': ies,'Module': modules, 'Reference': references, 'Usage': usage, 'Urls': urls} ], sort_keys=True, indent=4, separators=(',',':')) + "\n")
    ciod_module_rough.close()

def get_module_attr_raw(standard):
    module_table_pattern = re.compile(".*Module Attributes$")
    macro_pattern = re.compile(".*Include.*")
    module_table_divs = get_chapter_table_divs(standard, 'chapter_C')
    module_attr_rough = open('module_attr_rough.json', 'w')
    # Extract all the module description tables
    for tdiv in module_table_divs:
        data = []
        table_name = tdiv.p.strong.get_text()
        if (module_table_pattern.match(table_name)):
            table_body = tdiv.div.table.tbody
            table_data = extract_table_data(table_body)
            attr_names = []
            attr_tags = []
            attr_descriptions = []
            for row in table_data:
                try:
                    # Skip macros right now until we define a way to follow those links
                    if (macro_pattern.match(row[0])):
                        continue 
                    else:
                        attr_names.append(row[0])
                    attr_tags.append(row[1])
                    attr_descriptions.append(row[2])
                except IndexError:
                    module_attr_rough.write("Index error, table row not conforming to standard module-attribute structure.\n")

            module_attr_rough.write(json.dumps([table_name, {'Attribute Name': attr_names, 'Tag': attr_tags, 'Description': attr_descriptions} ], sort_keys=True, indent=4, separators=(',',':')) + "\n")
    module_attr_rough.close()

def extract_doc_links(table_body):
    data = []
    links = table_body.find_all('a')
    for link in links:
        if (link.get('href')):
            data.append(link.get('href'))
    return data

def extract_table_data(table_body):
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data

def get_chapter_table_divs(standard, chapter_name):
    table_divs = []
    chapter_divs = standard.find_all('div', class_='chapter')
    for chapter in chapter_divs:
        if (chapter.div.div.div.h1.a.get('id') == chapter_name):
            table_divs = chapter.find_all('div', class_='table')
            return table_divs

main()
