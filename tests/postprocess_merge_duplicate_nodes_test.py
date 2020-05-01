import pytest

from dicom_standard.postprocess_merge_duplicate_nodes import merge_duplicate_nodes


class TestMergeDuplicateNodes:
    def test_merge_duplicate_nodes(self):
        example_nodes = [
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'conditional': 'if Value Type is NUM.',
                'externalReferences': [{'title': 'Test Reference One'}],
            },
            {
                'path': 'module-one:00000001',
                'description': 'Node one duplicate.',
                'conditional': 'if Value Type is CODE.',
                'externalReferences': [{'title': 'Test Reference Two'}],
            },
        ]
        expected_node_list = [
            {
                'path': 'module-one:00000001',
                'description': '<p style="font-weight: bold">If Value Type is NUM:</p>Node one.<p style="font-weight: bold">If Value Type is CODE:</p>Node one duplicate.',
                'externalReferences': [
                    {'title': 'Test Reference One'},
                    {'title': 'Test Reference Two'},
                ],
            },
        ]
        assert merge_duplicate_nodes(example_nodes) == expected_node_list

    def test_merge_identical_description(self):
        example_nodes = [
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'conditional': 'if Value Type is NUM.',
                'externalReferences': [],
            },
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'conditional': 'if Value Type is CODE.',
                'externalReferences': [],
            },
        ]
        expected_node_list = [
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'externalReferences': [],
            },
        ]
        assert merge_duplicate_nodes(example_nodes) == expected_node_list

    def test_non_duplicate_nodes(self):
        example_nodes = [
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'conditional': None,
                'externalReferences': [],
            },
            {
                'path': 'module-one:00000002',
                'description': 'Node two.',
                'conditional': None,
                'externalReferences': [],
            },
        ]
        expected_node_list = [
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'externalReferences': [],
            },
            {
                'path': 'module-one:00000002',
                'description': 'Node two.',
                'externalReferences': [],
            },
        ]
        assert merge_duplicate_nodes(example_nodes) == expected_node_list

    def test_no_conditional_error(self):
        example_nodes = [
            {
                'path': 'module-one:00000001',
                'description': 'Node one.',
                'conditional': None,
                'externalReferences': [],
            },
            {
                'path': 'module-one:00000001',
                'description': 'Node one duplicate.',
                'conditional': None,
                'externalReferences': [],
            },
        ]
        expected_error_message = 'Duplicate attribute (path: module-one:00000001) ' \
                                 'has no conditional statement.'
        with pytest.raises(AssertionError) as e:
            merge_duplicate_nodes(example_nodes)
        assert str(e.value) == expected_error_message
