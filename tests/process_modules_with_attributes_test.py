from bs4 import BeautifulSoup

from dicom_standard.parse_lib import remove_attributes_from_html_tags


def test_remove_attributes_from_tag():
    tag = '''
        <p style="So much style">
            This is an
            <a href="coolsite" style="Some other cool style">
                awesome
            </a>
            <div>
                description
            </div>.
        </p>
    '''
    html = BeautifulSoup(tag, 'html.parser')
    top_level_tag = html.find('p')
    remove_attributes_from_html_tags(top_level_tag)
    assert top_level_tag.attrs == {}
    assert top_level_tag.find('a').attrs == {'href': 'coolsite'}
