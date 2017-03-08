from bs4 import BeautifulSoup

from parse_lib import remove_attributes_from_description_html, resolve_hrefs

def test_remove_attributes_from_tag():
    tag = '<p style="So much style">This is an <a href="coolsite" style="Some other cool style">awesome</a> <div>description</div>.</p>'
    html = BeautifulSoup(tag, 'html.parser')
    top_level_tag = html.find('p')
    new_top_level_tag = remove_attributes_from_description_html(top_level_tag)
    assert new_top_level_tag.attrs == {}
    assert new_top_level_tag.find('a').attrs == {'href': 'coolsite'}

def test_resolve_hrefs_in_description():
    tag = '<p style="So much style">This is an <a href="#coolAttribute" style="Some other cool style">awesome</a> <div>link to the standard</div>.</p>'
    html = BeautifulSoup(tag, 'html.parser')
    top_level_tag = html.find('p')
    top_level_tag_with_resolved_hrefs = resolve_hrefs(top_level_tag)
    assert top_level_tag_with_resolved_hrefs.find('a')['href'] == "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#coolAttribute"
