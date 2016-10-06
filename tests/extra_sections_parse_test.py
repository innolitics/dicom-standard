from bs4 import BeautifulSoup

import parse_extra_sections as p
import parse_lib as pl


def test_get_section_html():
    example_section_html = '''<div class="section"><div class="titlepage"><div><div><h5 class="title"><a id="sect_link"></a></h5></div></div></div></div>'''
    parseable_html = BeautifulSoup(example_section_html, 'html.parser')
    ref_section = p.html_string_from_reference('part03.html#sect_link', parseable_html)
    assert ref_section == example_section_html

def test_get_figure_html():
    example_figure_html = '''<div><a id="figure_link"></a><div><div><img src="figures/somefig.svg" /></div></div></div>'''
    corrected_figure_html = '''<div><a id="figure_link"></a><div><div><img src="http://dicom.nema.org/medical/dicom/current/output/html/figures/somefig.svg"/></div></div></div>'''
    parseable_html = BeautifulSoup(example_figure_html, 'html.parser')
    ref_section = p.html_string_from_reference('part03.html#figure_link', parseable_html)
    assert ref_section == corrected_figure_html

def test_expand_hrefs_part03():
    expandable_html = '''<div><a href="#something"></a></div>'''
    expanded_html = '''<div><a href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#something"></a></div>'''
    assert expanded_html == p.expand_resource_links_to_absolute(expandable_html)

def test_expand_hrefs_external():
    expandable_external_ref_html = '''<div><a href="part16.html#something"></a></div>'''
    expanded_external_ref_html = '''<div><a href="http://dicom.nema.org/medical/dicom/current/output/html/part16.html#something"></a></div>'''
    assert expanded_external_ref_html == p.expand_resource_links_to_absolute(expandable_external_ref_html)
