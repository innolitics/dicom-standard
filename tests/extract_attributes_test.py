from bs4 import BeautifulSoup

import dicom_standard.extract_attributes as ea

example_table = '''
<tbody>
    <tr><td>Data</td><td>inside</td><td>this</td><td>table</td></tr>
    <tr><td>should</td><td>be</td><td>a</td><td>list</td></tr>
</tbody
'''


def test_attribute_table_to_list():
    table = BeautifulSoup(example_table, 'html.parser')
    expected_table_list = [['Data', 'inside', 'this', 'table'],
                           ['should', 'be', 'a', 'list']]
    table_as_list_of_lists = ea.attribute_table_to_list(table)
    assert expected_table_list == table_as_list_of_lists
