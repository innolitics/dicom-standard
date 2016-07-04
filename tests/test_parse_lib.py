from parse_lib import left_join


def test_left_join_with_simple_dataset():
    left = [
        {'a': 1},
        {'a': 1},
        {'a': 2},
    ]

    right = {
        1: {'b': 'hello'},
        2: {'b': 'goodbye'},
    }

    expected_join = [
        {'a': 1, 'b': 'hello'},
        {'a': 1, 'b': 'hello'},
        {'a': 2, 'b': 'goodbye'},
    ]

    assert left_join(left, right, 'a') == expected_join
