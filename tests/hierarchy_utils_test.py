import hierarchy_utils as h

test_names = ['>>>name1', ' >space in front', '>>  \nstrange whitespace',
              '>>>>>>>>>>>>>>>>>>>> Long marker run', 'No markers']

def test_get_hierarchy_markers():
    expected_result = ['>>>', '>', '>>', '>>>>>>>>>>>>>>>>>>>>', '']
    results = list(map(h.get_hierarchy_markers, test_names))
    assert results == expected_result


def test_clean_field():
    expected_result = ['name1', 'space in front', 'strange whitespace',
                       'Long marker run', 'No markers']
    results = list(map(h.clean_field, test_names))
    assert results == expected_result


def test_add_attribute_parent_ids():
    test_table = {
        'id': 'test-table',
        'attributes': [
            {
                'name': 'Attribute 1',
                'id': '00010001',
                'type': 'None',
                'tag': '(0001,0001)',
            },
            {
                'name': '>Attribute 2',
                'id': '00010002',
                'type': 'None',
                'tag': '(0001,0002)',
            },
            {
                'name': '>>Attribute 3',
                'id': '00010003',
                'type': 'None',
                'tag': '(0001,0003)',
            },
        ]
    }
    test_table = h.record_hierarchy_for_module(test_table)
    assert test_table['attributes'][0]['id'] == 'test-table:00010001'
    assert test_table['attributes'][1]['id'] == 'test-table:00010001:00010002'
    assert test_table['attributes'][2]['id'] == 'test-table:00010001:00010002:00010003'


def test_add_parent_id_different_levels():
    test_table = {
        'id': 'test-table',
        'attributes': [
            {
                'name': 'Attribute 1',
                'id': '00010001',
                'type': 'None',
                'tag': '(0001,0001)',
            },
            {
                'name': '>Attribute 2',
                'id': '00010002',
                'type': 'None',
                'tag': '(0001,0002)',
            },
            {
                'name': '>>Attribute 3',
                'id': '00010003',
                'type': 'None',
                'tag': '(0001,0003)',
            },
            {
                'name': '>>>Attribute 4',
                'id': '00010004',
                'type': 'None',
                'tag': '(0001,0004)',
            },
            {
                'name': '>>Attribute 5',
                'id': '00010005',
                'type': 'None',
                'tag': '(0001,0005)',
            },
            {
                'name': '>Attribute 6',
                'id': '00010006',
                'type': 'None',
                'tag': '(0001,0006)',
            }
        ]
    }
    test_table = h.record_hierarchy_for_module(test_table)
    assert test_table['attributes'][0]['id'] == 'test-table:00010001'
    assert test_table['attributes'][1]['id'] == 'test-table:00010001:00010002'
    assert test_table['attributes'][2]['id'] == 'test-table:00010001:00010002:00010003'
    assert test_table['attributes'][3]['id'] == 'test-table:00010001:00010002:00010003:00010004'
    assert test_table['attributes'][4]['id'] == 'test-table:00010001:00010002:00010005'
    assert test_table['attributes'][5]['id'] == 'test-table:00010001:00010006'


def test_add_parent_id_small_sequences():
    test_table = {
        'id': 'test-table',
        'attributes': [
            {
                'name': 'Attribute 1',
                'id': '00010001',
                'type': 'None',
                'tag': '(0001,0001)',
            },
            {
                'name': '>Attribute 2',
                'id': '00010002',
                'type': 'None',
                'tag': '(0001,0002)',
            },
            {
                'name': '>>Attribute 3',
                'id': '00010003',
                'type': 'None',
                'tag': '(0001,0003)',
            },
            {
                'name': 'Attribute 4',
                'id': '00010004',
                'type': 'None',
                'tag': '(0001,0004)',
            },
            {
                'name': '>Attribute 5',
                'id': '00010005',
                'type': 'None',
                'tag': '(0001,0005)',
            },
            {
                'name': '>>Attribute 6',
                'id': '00010006',
                'tag': '(0001,0006)',
                'type': 'None',
            },
            {
                'name': '>Attribute 7',
                'id': '00010007',
                'type': 'None',
                'tag': '(0001,0007)',
            },
        ]
    }
    test_table = h.record_hierarchy_for_module(test_table)
    assert test_table['attributes'][0]['id'] == 'test-table:00010001'
    assert test_table['attributes'][1]['id'] == 'test-table:00010001:00010002'
    assert test_table['attributes'][2]['id'] == 'test-table:00010001:00010002:00010003'
    assert test_table['attributes'][3]['id'] == 'test-table:00010004'
    assert test_table['attributes'][4]['id'] == 'test-table:00010004:00010005'
    assert test_table['attributes'][5]['id'] == 'test-table:00010004:00010005:00010006'
    assert test_table['attributes'][6]['id'] == 'test-table:00010004:00010007'
