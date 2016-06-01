'''
parser.py

Parse the DICOM standard HTML file to extract the composite
IOD table, module table, attributes table, and their 
relationship tables.
'''

import json
import re
import sys

from bs4 import BeautifulSoup

def main(html_standard_path):
    html_doc = open(html_standard_path, 'r')
    standard = BeautifulSoup(html_doc, 'html.parser')
    get_ciod_module_raw(standard)
    get_module_attr_raw(standard)
    html_doc.close()

def get_ciod_module_raw(standard):
    iod_table_pattern = re.compile(".*IOD Modules$")
    ciod_table_divs = get_chapter_table_divs(standard, 'chapter_A')
    # Extract all the composite IOD tables 
    ciod_module_rough = open('tmp/ciod_module_rough.json', 'w')
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
            json_list = [table_name]
            for i in range (len(ies)):
                json_list.append({'IE Name': ies[i], 'Module': modules[i], 'Doc Reference': references[i], 'Usage': usage[i], 'URL':urls[i]})
            ciod_module_rough.write(json.dumps(json_list, sort_keys=True, indent=4, separators=(',',':')) + "\n")
    ciod_module_rough.close()

def get_module_attr_raw(standard):
    module_table_pattern = re.compile(".*Module Attributes$")
    basic_entry_header_pattern = re.compile(".*BASIC CODED ENTRY ATTRIBUTES$")
    enhanced_encoding_header_pattern = re.compile(".*ENHANCED ENCODING MODE$")
    link_pattern = re.compile(".*Include.*")
    all_tables = standard.find_all('div', class_='table')
    module_table_divs = get_chapter_table_divs(standard, 'chapter_C')
    module_attr_rough = open('tmp/module_attr_rough.json', 'w')
    # Extract all the module description tables
    for tdiv in module_table_divs:
        data = []
        table_name = tdiv.p.strong.get_text()
        if (module_table_pattern.match(table_name)):
            table_body = tdiv.div.table.tbody
            table_data = extract_table_data(table_body)
            attr_names = []
            attr_tags = []
            attr_types = []
            attr_descriptions = []
            ref_links = get_include_links(table_body)
            i = 0
            for row in table_data:
                try:
                    # There seem to be only two headers like this in the whole standard. They break form, so 
                    # we catch them with a regex match.
                    if (basic_entry_header_pattern.match(row[0]) or enhanced_encoding_header_pattern.match(row[0])):
                        i += 1
                        continue
                    if (ref_links[i] is not None):
                        a_name, a_tag, a_type, a_descrip = get_linked_attrs(all_tables, ref_links[i])
                        attr_names.extend(a_name)
                        attr_tags.extend(a_tag)
                        attr_types.extend(a_type)
                        attr_descriptions.extend(a_descrip)
                        i += 1
                        continue
                    else:
                        attr_names.append(row[0])
                    attr_tags.append(row[1])
                    j = 2
                    if (len(row) < 4):
                        attr_types.append(None)     
                    else:
                        attr_types.append(row[j])
                        j += 1
                    attr_descriptions.append(row[j])
                except IndexError:
                    module_attr_rough.write("Index error, table row not conforming to standard module-attribute structure.\n")
                    # Catch errors and insert None into each field as a placeholder.
                    if (len(attr_names)-1 == i):
                        attr_names[len(attr_names)-1] = None
                    else:
                        attr_names.append(None)
                    if (len(attr_tags)-1 == i):
                        attr_tags[len(attr_tags)-1] = None
                    else:
                        attr_tags.append(None)
                    if (len(attr_types)-1 == i):
                        attr_types[len(attr_types)-1] = None
                    else:
                        attr_types.append(None)
                    if (len(attr_descriptions)-1 == i):
                        attr_descriptions[len(attr_descriptions)-1] = None
                    else:
                        attr_descriptions.append(None)
                i += 1

            json_list = [table_name]
            for i in range (len(attr_descriptions)):
                json_list.append({'Attribute:': attr_names[i], 'Tag': attr_tags[i], 'Type': attr_types[i], 'Description': attr_descriptions[i]});
            module_attr_rough.write(json.dumps(json_list, sort_keys=True, indent=4, separators=(',',':')) + "\n")
    module_attr_rough.close()

def get_linked_attrs(all_tables, ref_id):
    basic_entry_header_pattern = re.compile(".*BASIC CODED ENTRY ATTRIBUTES$")
    enhanced_encoding_header_pattern = re.compile(".*ENHANCED ENCODING MODE$")
    attr_names = []
    attr_tags = []
    attr_types = []
    attr_descriptions = []
    for table in all_tables:
        if (table.a.get('id') == ref_id):
            table_body = table.div.table.tbody
            table_data = extract_table_data(table_body)
            ref_links = get_include_links(table_body)
            # Prevent an infinitely recursive reference
            for i in range(len(ref_links)):
                if (ref_links[i] == ref_id):
                    ref_links[i] = None
            i = 0
            for row in table_data:
                # There seem to be only two headers like this in the whole standard. They break form, so 
                # we catch them with a specific regex match.
                if (basic_entry_header_pattern.match(row[0]) or enhanced_encoding_header_pattern.match(row[0])):
                    i += 1
                    continue
                if (ref_links[i] is not None):
                    a_name, a_tag, a_type, a_descrip = get_linked_attrs(all_tables, ref_links[i])
                    attr_names.extend(a_name)
                    attr_tags.extend(a_tag)
                    attr_types.extend(a_type)
                    attr_descriptions.extend(a_descrip)
                    i += 1
                    continue
                else:
                    attr_names.append(row[0])
                attr_tags.append(row[1])
                j = 2
                if (len(row) < 4):
                    attr_types.append(None)     
                else:
                    attr_types.append(row[j])
                    j += 1
                attr_descriptions.append(row[j])
                i += 1
    return (attr_names, attr_tags, attr_types, attr_descriptions) 

# Generate a list containing the href for every include link for each table row.
# If a table row doesn't have an href, the list contains a placeholder None
def get_include_links(table_body):
    link_pattern = re.compile('.*Include.*')
    ref_links = []
    rows = table_body.find_all('tr')
    for row in rows:
        appended = False
        cols = row.find_all('td')
        for col in cols:
            try:
                span_text = col.p.span
                # If we find a span with "Include" and a link, we've found one!
                #if ((span_text is not None) and (span_text.a is not None)):
                if ((span_text.a is not None) and (link_pattern.match(span_text.get_text()))):
                    ref_links.append(span_text.a.get('href'))
                    appended = True
                    break
            except AttributeError:
                continue
        if not appended:
            ref_links.append(None)
    # Separate the div ID from the URL
    i = 0
    for link in ref_links:
        if link:
            _url, _pound, table_id = link.partition('#')
            if table_id is None:
                print("URL formatting error")
            ref_links[i] = table_id
        i += 1    
    return ref_links

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

if __name__ == '__main__':
    if sys.argv[1] is not None:
        main(sys.argv[1])
    else:
        print("No DICOM standard HTML file path specified. Please pass a path to the script.")
