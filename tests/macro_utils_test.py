import macro_utils as m

example_include_statement = '''
<p>&gt;&gt; Include <a href="#somemacro"class="xref">Table somemacro</a></p>
'''

def test_is_macro_row():
    example_macro_row = {
        'tag': 'None',
        'name': example_include_statement
    }
    example_normal_row = {
        'tag': '(0001,0001)',
        'name': '<p>&gt;&gt; Some Attribute</p>'
    }
    assert m.is_macro_row(example_macro_row)
    assert not m.is_macro_row(example_normal_row)


def test_flatten_one_layer():
    a = [[1, 2, 3], [4, 5, 6]]
    assert m.flatten_one_layer(a) == [1, 2, 3, 4, 5, 6]


def test_referenced_macro_id_from_include_statement():
    assert m.referenced_macro_id_from_include_statement(example_include_statement) == 'somemacro'


def test_update_attribute_hierarchy_levels():
    example_attributes = [
        {'name': '<td>name1</td>'},
        {'name': '<td>name2</td>'},
        {'name': '<td>name3</td>'},
    ]
    expected_attributes = [
        {'name': '<td>&gt;&gt;name1</td>'},
        {'name': '<td>&gt;&gt;name2</td>'},
        {'name': '<td>&gt;&gt;name3</td>'},
    ]
    assert m.update_attribute_hierarchy_levels(example_attributes, '>>') == expected_attributes
