'''
Utility functions for managing the hierarchy structure of
attributes in the module-attribute relationship tables
'''
import re

def get_hierarchy_markers(name):
    clean_name = name.strip()
    _, *split = re.split('^(>+)', clean_name)
    return '' if split == [] else split[0]

def get_hierarchy_level(name):
    return len(get_hierarchy_markers(name))

def clean_field(name):
    return re.sub(r'[>]', '', name).strip()
