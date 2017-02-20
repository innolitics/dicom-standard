'''
Utility functions for managing the hierarchy structure of
attributes in the module-attribute relationship tables
'''
import re

def get_hierarchy_level(name):
    clean_name = name.strip()
    preceding_space, *split = re.split('^(>+)', clean_name)
    if split == []:
        indicator = ''
    else:
        indicator = split[0]
    return indicator
