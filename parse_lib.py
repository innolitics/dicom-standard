'''
parse_lib.py

Common functions for extracting information from the 
DICOM standard HTML file.
'''

import re

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
