import sys
import re
import os

from dicom_standard.parse_lib import parse_html_file, write_pretty_json

REFERENCED_IDS_RE = re.compile(r'(sect.*)|(figure.*)|(biblio.*)|(table.*)|(note.*)')


def extract_section_ids(standard):
    return {page: referenced_id_anchors(html) for page, html in standard.items()}


def referenced_id_anchors(html):
    return html.find_all('a', attrs={'id': REFERENCED_IDS_RE})


def section_html_from_id_anchor(reference_id_anchor):
    if re.match(r'(sect.*)|(biblio.*)|(table.*)|(note.*)|(figure.*)', reference_id_anchor['id']):
        return enclosing_section_from_id(reference_id_anchor)
    else:
        raise Exception(reference_id_anchor.parent + " didn't match a known pattern.")


def normalize_sections(all_sections):
    return {section['id']: str(section_html_from_id_anchor(section)) for section in all_sections}


def enclosing_section_from_id(id_div):
    # TODO: put example from the standard here
    if re.match(r'sect.*', id_div['id']):
        return id_div.parent.parent.parent.parent.parent
    elif re.match(r'biblio.*', id_div['id']):
        return id_div.parent.parent.parent
    elif re.match(r'table.*', id_div['id']):
        return id_div.parent.parent
    elif re.match(r'note.*', id_div['id']):
        return id_div.parent.parent.parent.parent.parent.parent
    else:
        return id_div.parent.parent


if __name__ == '__main__':
    # TODO: figure out a way to speed up the parsing; since we only need a
    # small portion of the parse tree, we may be able to use:
    # https://docs.python.org/3/library/html.parser.html to avoid building the
    # full parse tree.
    standard = {os.path.basename(f): parse_html_file(f) for f in sys.argv[1:]}
    section_ids = extract_section_ids(standard)
    sections = {page: normalize_sections(html) for page, html in section_ids.items()}
    write_pretty_json(sections)
