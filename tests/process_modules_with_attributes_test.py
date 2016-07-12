from process_modules_with_attributes import add_attribute_parent_ids, find_non_adjacent_parent, record_parent_id_to_attribute


def test_add_attribute_parent_ids():
    test_attributes = [
        {
            'name': 'Attribute 1',
            'id': '0001-0001',
            'tag': '(0001,0001)',
        },
        {
            'name': '>Attribute 2',
            'id': '0001-0002',
            'tag': '(0001,0002)',
        },
        {
            'name': '>>Attribute 3',
            'id': '0001-0003',
            'tag': '(0001,0003)',
        },
    ]
    add_attribute_parent_ids(test_attributes)
    assert test_attributes[0]['parent_id'] is None
    assert test_attributes[1]['parent_id'] == '0001-0001'
    assert test_attributes[2]['parent_id'] == '0001-0001:0001-0002'


def test_add_parent_id_different_levels():
    test_attributes = [
        {
            'name': 'Attribute 1',
            'id': '0001-0001',
            'tag': '(0001,0001)',
        },
        {
            'name': '>Attribute 2',
            'id': '0001-0002',
            'tag': '(0001,0002)',
        },
        {
            'name': '>>Attribute 3',
            'id': '0001-0003',
            'tag': '(0001,0003)',
        },
        {
            'name': '>>>Attribute 4',
            'id': '0001-0004',
            'tag': '(0001,0004)',
        },
        {
            'name': '>>Attribute 5',
            'id': '0001-0005',
            'tag': '(0001,0005)',
        },
        {
            'name': '>Attribute 6',
            'id': '0001-0006',
            'tag': '(0001,0006)',
        }
    ]
    add_attribute_parent_ids(test_attributes)
    assert test_attributes[0]['parent_id'] is None
    assert test_attributes[1]['parent_id'] == '0001-0001'
    assert test_attributes[2]['parent_id'] == '0001-0001:0001-0002'
    assert test_attributes[3]['parent_id'] == '0001-0001:0001-0002:0001-0003' 
    assert test_attributes[4]['parent_id'] == '0001-0001:0001-0002'
    assert test_attributes[5]['parent_id'] == '0001-0001'


def test_add_parent_id_small_sequences():
    test_attributes = [
        {
            'name': 'Attribute 1',
            'id': '0001-0001',
            'tag': '(0001,0001)',
        },
        {
            'name': '>Attribute 2',
            'id': '0001-0002',
            'tag': '(0001,0002)',
        },
        {
            'name': '>>Attribute 3',
            'id': '0001-0003',
            'tag': '(0001,0003)',
        },
        {
            'name': 'Attribute 4',
            'id': '0001-0004',
            'tag': '(0001,0004)',
        },
        {
            'name': '>Attribute 5',
            'id': '0001-0005',
            'tag': '(0001,0005)',
        },
        {
            'name': '>Attribute 6',
            'id': '0001-0006',
            'tag': '(0001,0006)',
        }
    ]
    add_attribute_parent_ids(test_attributes)
    assert test_attributes[0]['parent_id'] is None
    assert test_attributes[1]['parent_id'] == '0001-0001'
    assert test_attributes[2]['parent_id'] == '0001-0001:0001-0002'
    assert test_attributes[3]['parent_id'] is None
    assert test_attributes[4]['parent_id'] == '0001-0004'
    assert test_attributes[5]['parent_id'] == '0001-0004'


def test_find_non_adjacent_parent():
    attribute_list = [
        {
            'name': 'Attribute 1',
            'id': '0001-0001',
            'parent_id': None,
            'tag': '(0001,0001)',
        },
        {
            'name': '>Attribute 2',
            'id': '0001-0002',
            'parent_id': '0001-0001',
            'tag': '(0001,0002)',
        },
        {
            'name': '>>Attribute 3',
            'id': '0001-0003',
            'parent_id': '0001-0003',
            'tag': '(0001,0003)',
        },
        {
            'name': '>Attribute 4',
            'id': '0001-0004',
            'parent_id': '0001-0004',
            'tag': '(0001,0004)',
        }    
    ]
    previous_attribute = {
        'id': '0001-0003',
        'sequence_indicator': '>>',
        'parent_id': '0001-0002' 
    }
    parent_id = find_non_adjacent_parent('>', previous_attribute, attribute_list)
    assert parent_id == '0001-0001'


def test_find_adjacent_parent():
    attribute_list = [
        {
            'name': 'Attribute 1',
            'id': '0001-0001',
            'parent_id': None,
            'tag': '(0001,0001)',
        },
        {
            'name': '>Attribute 2',
            'id': '0001-0002',
            'parent_id': '0001-0001',
            'tag': '(0001,0002)',
        }
    ]
    previous_attribute = {
        'id': '0001-0001',
        'sequence_indicator': '',
        'parent_id': None 
    }
    parent_id = record_parent_id_to_attribute('>', previous_attribute, attribute_list)
    assert parent_id == '0001-0001'


def test_find_adjacent_parent_with_preceding_sibling_elements():
    attribute_list = [
        {
            'name': 'Attribute 1',
            'id': '0001-0001',
            'parent_id': None,
            'tag': '(0001,0001)',
            'order': 0
        },
        {
            'name': '>Attribute 2',
            'id': '0001-0002',
            'parent_id': '0001-0001',
            'tag': '(0001,0002)',
            'order': 1
        },
        {
            'name': '>Attribute 3',
            'id': '0001-0003',
            'parent_id': '0001-0001',
            'tag': '(0001,0003)',
            'order': 1
        }
    ]
    previous_attribute = {
        'id': '0001-0002',
        'sequence_indicator': '>',
        'parent_id': '0001-0001' 
    }
    parent_id = record_parent_id_to_attribute('>', previous_attribute, attribute_list)
    assert parent_id == '0001-0001'
