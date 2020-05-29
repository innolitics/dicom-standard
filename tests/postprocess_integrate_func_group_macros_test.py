from dicom_standard.postprocess_integrate_func_group_macros import (
    update_description,
    process_mffg_macro_attributes,
    process_cffg_macro_attributes,
    process_fg_attributes,
)
from dicom_standard.process_modules import MF_FUNC_GROUP_MODULE_ID, CF_FUNC_GROUP_MODULE_ID

example_macro_attrs = [
    {
        'macroId': 'example-macro-1',
        'path': 'example-macro-1:0001',
        'description': 'Attribute of Example Macro 1.'
    },
    {
        'macroId': 'example-macro-1',
        'path': 'example-macro-1:0001:0002',
        'description': 'Sub-attribute of Example Macro 1.'
    },
]
example_macro = {
    'macroName': 'Example Macro 1',
    'ciodId': 'example-ciod',
    'macroId': 'example-macro-1',
    'usage': 'C',
    'conditionalStatement': 'Required if Test Macro present.',
}


def test_update_description_adds_period_to_conditional():
    example_attr = {
        'macroId': 'example-macro-1',
        'path': 'example-macro-1:0001',
        'description': 'Attribute of Example Macro 1.'
    }
    example_macro_without_period = {
        'macroName': 'Example Macro 1',
        'usage': 'C',
        'conditionalStatement': 'Conditional without period',
    }
    expected_updated_conditonal = 'Conditional without period.'
    update_description(example_attr, example_macro_without_period)
    assert expected_updated_conditonal in example_attr['description']


def test_process_mffg_macro_attributes():
    expected_processed_attrs = [
        {
            'moduleId': 'example-ciod-multi-frame-functional-groups',
            'path': 'example-ciod-multi-frame-functional-groups:52009229:0001',
            'description': 'Attribute of Example Macro 1.<h3>Note</h3>'
                           '<p>Part of the Example Macro 1 Functional Group Macro with usage: C</p>'
                           '<p>Required if Test Macro present.</p>'
        },
        {
            'moduleId': 'example-ciod-multi-frame-functional-groups',
            'path': 'example-ciod-multi-frame-functional-groups:52009230:0001',
            'description': 'Attribute of Example Macro 1.<h3>Note</h3>'
                           '<p>Part of the Example Macro 1 Functional Group Macro with usage: C</p>'
                           '<p>Required if Test Macro present.</p>'
        },
        {
            'moduleId': 'example-ciod-multi-frame-functional-groups',
            'path': 'example-ciod-multi-frame-functional-groups:52009229:0001:0002',
            'description': 'Sub-attribute of Example Macro 1.<h3>Note</h3>'
                           '<p>Part of the Example Macro 1 Functional Group Macro with usage: C</p>'
                           '<p>Required if Test Macro present.</p>'
        },
        {
            'moduleId': 'example-ciod-multi-frame-functional-groups',
            'path': 'example-ciod-multi-frame-functional-groups:52009230:0001:0002',
            'description': 'Sub-attribute of Example Macro 1.<h3>Note</h3>'
                           '<p>Part of the Example Macro 1 Functional Group Macro with usage: C</p>'
                           '<p>Required if Test Macro present.</p>'
        },
    ]
    assert process_mffg_macro_attributes(example_macro_attrs, example_macro) == expected_processed_attrs


def test_process_cffg_macro_attributes():
    expected_processed_attrs = [
        {
            'moduleId': 'example-ciod-current-frame-functional-groups',
            'path': 'example-ciod-current-frame-functional-groups:00060001:0001',
            'description': 'Attribute of Example Macro 1.<h3>Note</h3>'
                           '<p>Part of the Example Macro 1 Functional Group Macro with usage: C</p>'
                           '<p>Required if Test Macro present.</p>'
        },
        {
            'moduleId': 'example-ciod-current-frame-functional-groups',
            'path': 'example-ciod-current-frame-functional-groups:00060001:0001:0002',
            'description': 'Sub-attribute of Example Macro 1.<h3>Note</h3>'
                           '<p>Part of the Example Macro 1 Functional Group Macro with usage: C</p>'
                           '<p>Required if Test Macro present.</p>'
        },
    ]
    assert process_cffg_macro_attributes(example_macro_attrs, example_macro) == expected_processed_attrs


def test_process_fg_attributes():
    example_ciods = ['example-ciod-1', 'example-ciod-2']
    example_module_to_attr = [
        {
            'moduleId': 'multi-frame-functional-groups',
            'path': 'multi-frame-functional-groups:0001',
        },
        {
            'moduleId': 'multi-frame-functional-groups',
            'path': 'multi-frame-functional-groups:0001:0002',
        },
        {
            'moduleId': 'current-frame-functional-groups',
            'path': 'current-frame-functional-groups:1001',
        },
    ]
    expected_processed_mffg_attrs = [
        {
            'moduleId': 'example-ciod-1-multi-frame-functional-groups',
            'path': 'example-ciod-1-multi-frame-functional-groups:0001',
        },
        {
            'moduleId': 'example-ciod-1-multi-frame-functional-groups',
            'path': 'example-ciod-1-multi-frame-functional-groups:0001:0002',
        },
        {
            'moduleId': 'example-ciod-2-multi-frame-functional-groups',
            'path': 'example-ciod-2-multi-frame-functional-groups:0001',
        },
        {
            'moduleId': 'example-ciod-2-multi-frame-functional-groups',
            'path': 'example-ciod-2-multi-frame-functional-groups:0001:0002',
        },
    ]
    expected_processed_cffg_attrs = [
        {
            'moduleId': 'example-ciod-1-current-frame-functional-groups',
            'path': 'example-ciod-1-current-frame-functional-groups:1001',
        },
        {
            'moduleId': 'example-ciod-2-current-frame-functional-groups',
            'path': 'example-ciod-2-current-frame-functional-groups:1001',
        },
    ]
    assert process_fg_attributes(example_module_to_attr, example_ciods, MF_FUNC_GROUP_MODULE_ID) == expected_processed_mffg_attrs
    assert process_fg_attributes(example_module_to_attr, example_ciods, CF_FUNC_GROUP_MODULE_ID) == expected_processed_cffg_attrs
