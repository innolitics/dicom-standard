'''
parse_standard.py

Parse the DICOM standard HTML file to extract the composite
IOD table, module table, attributes table, and their 
relationship tables.
'''

import sys
import pickle

from bs4 import BeautifulSoup

import parse_lib

def main(html_standard_path, output_path):
    with open(output_path, 'wb') as parsable_standard:
        html_doc = open(html_standard_path, 'r')
        standard = BeautifulSoup(html_doc, 'html.parser')
        html_doc.close()


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Not enough arguments specified. Please pass a path to the standard AND an output path for the parse object.")
