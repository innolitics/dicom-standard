'''
parse_lib.py

Common functions for extracting information from the 
DICOM standard HTML file.
'''

import re

def separate_table_data(table_body, fields, standard=None, hanging_indent=False, follow_links=False, current_ref=None):
    table_data = extract_table_data(table_body)
    num_columns = len(fields)
    field_data = [[] for i in fields]

    include_links = None
    all_tables = None
    if follow_links:
        include_links = get_include_links(table_body)
        if (standard is None):
            raise TypeError('Did not supply standard parse object when follow_links is True')
        all_tables = standard.find_all('div', class_='table')
        # Prevent infinite recursion
        if (current_ref is not None):
            for k in range(len(include_links)):
                if (include_links[k] == current_ref):
                    include_links[k] = None

    # if ((num_columns != len(table_data[0])) and (num_columns-1 != len(table_data[0]))):
        # raise TypeError('Incorrect fields supplied for this table.')

    previous_row = table_data[0][0]
    row_idx = -1
    for row in table_data:
        row_idx += 1
        i = 0
        j = 0

        # Special Cases
        if hanging_indent:
            if (one_less_column(row, fields)):
                field_data[j].append(previous_row)
            else:
                field_data[j].append(row[i])
                previous_row = row[i]
                i += 1
            j += 1

        elif follow_links:
            if blacklisted_row(row, include_links[row_idx], num_columns):
                row_idx -= 1
                continue
            if (include_links[row_idx] is not None):
                # Recursion!
                new_table = find_sub_table_body(all_tables, include_links[row_idx])
                subfield_data = separate_table_data(new_table, fields, standard, hanging_indent=False, follow_links=True, current_ref=include_links[row_idx])
                for k in range(len(subfield_data)):
                    field_data[k].extend(subfield_data[k])
                continue 

        for j in range(j,num_columns):
            if (follow_links and (j == 2) and (one_less_column(row, fields))):
                field_data[j].append(None)
                continue
            field_data[j].append(row[i])
            i += 1

    return field_data

def blacklisted_row(row, link, num_columns):
    if ((len(row) != num_columns) and (len(row) != num_columns - 1) and (link is None)):
        return True
    basic_entry_header_pattern = re.compile(".*BASIC CODED ENTRY ATTRIBUTES$")
    enhanced_encoding_header_pattern = re.compile(".*ENHANCED ENCODING MODE$")
    non_table_pattern = re.compile("^sect.*")
    if ((link is not None) and non_table_pattern.match(link)):
        return True
    if (basic_entry_header_pattern.match(row[0]) or enhanced_encoding_header_pattern.match(row[0])):
        return True
    return False

def find_sub_table_body(all_tables, table_id):
    for table in all_tables:
        if (table.a.get('id') == table_id):
            return table.div.table.tbody
    print(table_id)
    return None

def one_less_column(row, fields):
    if (len(row) == len(fields)-1):
        return True;
    else:
        return False;

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
