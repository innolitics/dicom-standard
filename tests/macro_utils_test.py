import dicom_standard.macro_utils as m

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


def test_update_attribute_hierarchy_markers():
    example_attributes = [
        {'name': '<td>name1</td>'},
        {'name': '<td>&gt;name2</td>'},
        {'name': '<td>&gt;&gt;name3</td>'},
    ]
    expected_attributes = [
        {'name': '<td>&gt;&gt;name1</td>'},
        {'name': '<td>&gt;&gt;&gt;name2</td>'},
        {'name': '<td>&gt;&gt;&gt;&gt;name3</td>'},
    ]
    assert m.update_attribute_hierarchy_markers(example_attributes, '>>') == expected_attributes


def test_insert_nested_macro():
    mock_table = {
        'linkToStandard': 'http://somelink#table-id',
        'name': 'mock-table',
        'attributes': [
            {
                'name': '<td>Attribute 1</td>',
                'type': 'None',
                'tag': '00010001',
                'description': 'something'
            },
            {
                'name': '<td>&gt;Include <a href="#somemacro" class="xref">Table Otherthing</a></td>',
                'type': 'None',
                'tag': 'None',
                'description': 'None'
            }
        ]
    }

    mock_macros = {
        "somemacro": {
            'linkToStandard': 'http://somelink#somemacro',
            'name': 'mock-macro',
            'attributes': [
                {
                    'name': '<td>Attribute 1a</td>',
                    'type': 'None',
                    'tag': '00010002',
                    'description': 'some attribute in a macro'
                },
                {
                    'name': '<td>&gt;Attribute 1e</td>',
                    'type': 'None',
                    'tag': '00010005',
                    'description': 'some nested attribute in a macro'
                },
                {
                    'name': '<td>&gt;&gt;Include <a href="#somemacro2" class="xref">Table Otherthing2</a></td>',
                    'type': 'None',
                    'tag': 'None',
                    'description': 'None'
                }
            ]
        },
        "somemacro2": {
            'linkToStandard': 'http://somelink#somemacro2',
            'name': 'mock-macro-2',
            'attributes': [
                {
                    'name': '<td>Attribute 1b</td>',
                    'type': 'None',
                    'tag': '00010003',
                    'description': 'some other attribute in a macro'
                },
                {
                    'name': '<td>&gt;Attribute 1c</td>',
                    'type': 'None',
                    'tag': '00010004',
                    'description': 'some final attribute in a macro'
                }
            ]
        }
    }

    expected_attributes = [
        {
            'name': '<td>Attribute 1</td>',
            'type': 'None',
            'tag': '00010001',
            'description': 'something'
        },
        {
            'name': '<td>&gt;Attribute 1a</td>',
            'type': 'None',
            'tag': '00010002',
            'description': 'some attribute in a macro'
        },
        {
            'name': '<td>&gt;&gt;Attribute 1e</td>',
            'type': 'None',
            'tag': '00010005',
            'description': 'some nested attribute in a macro'
        },
        {
            'name': '<td>&gt;&gt;&gt;Attribute 1b</td>',
            'type': 'None',
            'tag': '00010003',
            'description': 'some other attribute in a macro'
        },
        {
            'name': '<td>&gt;&gt;&gt;&gt;Attribute 1c</td>',
            'type': 'None',
            'tag': '00010004',
            'description': 'some final attribute in a macro'
        }
    ]

    assert m.expand_macro_rows(mock_table, mock_macros) == expected_attributes
