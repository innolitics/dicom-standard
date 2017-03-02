from hierarchy_utilities import get_hierarchy_markers

def test_hierarchy_level_extraction():
    indicators = ['>>>I am three levels down.',
                  '   >>  I am two levels down with spaces.',
                  '   I am at the top!',
                  '>>>>>>>>>>I am very far down.']
    expected_results = ['>>>', '>>', '', '>>>>>>>>>>']
    results = list(map(get_hierarchy_markers, indicators))
    assert results == expected_results
