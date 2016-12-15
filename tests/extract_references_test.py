from bs4 import BeautifulSoup

import extract_references


def test_get_section_html():
    example_section_html = '''<div class="section"><div class="titlepage"><div><div><h5 class="title"><a id="sect_link"></a></h5></div></div></div></div>'''
    parseable_html = BeautifulSoup(example_section_html, 'html.parser')
    ref_section = extract_references.html_string_from_reference('part03.html#sect_link', parseable_html)
    assert ref_section == example_section_html

def test_get_figure_html():
    example_figure_html = '''<div><a id="figure_link"></a><div><div><img src="figures/somefig.svg" /></div></div></div>'''
    corrected_figure_html = '''<div><a id="figure_link"></a><div><div><img src="http://dicom.nema.org/medical/dicom/current/output/html/figures/somefig.svg"/></div></div></div>'''
    parseable_html = BeautifulSoup(example_figure_html, 'html.parser')
    ref_section = extract_references.html_string_from_reference('part03.html#figure_link', parseable_html)
    assert ref_section == corrected_figure_html

def test_expand_hrefs_part03():
    expandable_html = '''<div><a href="#something"></a></div>'''
    expanded_html = '''<div><a href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#something"></a></div>'''
    assert expanded_html == extract_references.expand_resource_links_to_absolute(expandable_html)

def test_expand_hrefs_external():
    expandable_external_ref_html = '''<div><a href="part16.html#something"></a></div>'''
    expanded_external_ref_html = '''<div><a href="http://dicom.nema.org/medical/dicom/current/output/html/part16.html#something"></a></div>'''
    assert expanded_external_ref_html == extract_references.expand_resource_links_to_absolute(expandable_external_ref_html)

def test_remove_attributes():
    tag_with_attrs = '''<a href="somelink" style="lots-of-style: good-thing;" class="classy" onClick="doCoolThings">Some cool link</a>'''
    tag_without_attrs = '''<a class="classy" href="somelink">Some cool link</a>'''
    parseable_html = BeautifulSoup(tag_with_attrs, 'html.parser')
    parseable_tag = parseable_html.find('a')
    assert str(extract_references.remove_attributes(parseable_tag)) == tag_without_attrs

def test_clean_simple_html_string():
    dirty_html = '''<div class="something" style="some-styling: always_good;" madeup="this isn't even legit"><a href="cool_link" style="fun">Hello!</a></div>'''
    clean_html = '''<div class="something"><a href="cool_link">Hello!</a></div>'''
    assert extract_references.clean_html_string(dirty_html) == clean_html

def test_clean_nested_html_string():
    dirty_html = '''<div class="something" style="some-styling: always_good;" madeup="this isn't even legit"><a href="cool_link" style="fun"><span style="margin-left: 10x;">Why</span> Hello!</a><img src="some_source"/></div>'''
    clean_html = '''<div class="something"><a href="cool_link"><span>Why</span> Hello!</a><img src="some_source"/></div>'''
    assert extract_references.clean_html_string(dirty_html) == clean_html
