import pytest
import subprocess

import parse_lib as pl

@pytest.mark.endtoend
@pytest.fixture(scope='module')
def make_standard():
    subprocess.run(['make', 'all', '--jobs', '4'])

@pytest.mark.endtoend
@pytest.fixture(scope='module')
def ciods(make_standard):
    return pl.read_json_to_dict('dist/ciods.json')

@pytest.mark.endtoend
@pytest.fixture(scope='module')
def modules(make_standard):
    return pl.read_json_to_dict('dist/modules.json')

@pytest.mark.endtoend
@pytest.fixture(scope='module')
def attributes(make_standard):
    return pl.read_json_to_dict('dist/attributes.json')

@pytest.mark.endtoend
@pytest.fixture(scope='module')
def ciod_module_relationship(make_standard):
    return pl.read_json_to_dict('dist/ciod_to_modules.json')

@pytest.mark.endtoend
@pytest.fixture(scope='module')
def module_attribute_relationship(make_standard):
    return pl.read_json_to_dict('dist/module_to_attributes.json')

@pytest.mark.endtoend
def test_total_number_ciods(ciods):
    defined_ciods = 119
    assert len(ciods) == defined_ciods 

@pytest.mark.endtoend
def test_total_number_attributes(attributes):
    defined_valid_attributes = 4084
    assert len(attributes) == defined_valid_attributes

@pytest.mark.endtoend
def test_valid_foreign_keys_ciod_module(ciod_module_relationship, ciods, modules):
    for pair in ciod_module_relationship:
        assert pair['ciod'] in ciods 
        assert pair['module'] in modules

@pytest.mark.endtoend
def test_valid_foreign_keys_module_attribute(module_attribute_relationship, modules, attributes):
    for pair in module_attribute_relationship:
        assert pair['module'] in modules
        assert pair['tag'] in attributes

@pytest.mark.endtoend
def test_vertical_samples_from_standard(ciods, modules, attributes):
    test_ciod = {
        "us-multi-frame-image": {
            "description": "The Ultrasound (US) Multi-frame Image Information Object Definition specifies a Multi-frame image that has been created by an ultrasound imaging device.",
            "link_to_standard": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.7-1",
            "name": "US Multi-frame Image"
        }
    }
    test_module = {
        "patient": {
            "name": "Patient",
            "link_to_standard": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-1"
        }
    }
    test_attribute = {
        "(0010,0010)": {
            "slug": "0010-0010",
            "retired": False,
            "keyword": "PatientName",
            "name": "Patient's Name",
            "value_multiplicity": "1",
            "value_representation": "PN"
        },
        "(0008,0034)": {
            "slug": "0008-0034",
            "retired": True,
            "keyword": "OverlayTime",
            "name": "Overlay Time",
            "value_multiplicity": "1", 
            "value_representation": "TM"
        },
        "(0008,0108)": {
            "slug": "0008-0108",
            "retired": False,
            "keyword": "ExtendedCodeMeaning",
            "name": "Extended Code Meaning",
            "value_multiplicity": "1", 
            "value_representation": "LT"
        }
    }
    assert test_ciod["us-multi-frame-image"] == ciods["us-multi-frame-image"] 
    assert test_module["patient"] == modules["patient"] 
    assert test_attribute["(0010,0010)"] == attributes["(0010,0010)"]
    assert test_attribute["(0008,0034)"] == attributes["(0008,0034)"]
    assert test_attribute["(0008,0108)"] == attributes["(0008,0108)"]

@pytest.mark.endtoend
def test_trace_from_attribute_to_ciod(ciods, ciod_module_relationship,
        modules, module_attribute_relationship, attributes):
    attr = {
        "(0008,0121)": {
            "name":"Equivalent Code Sequence",
            "retired": False,
            "value_multiplicity":"1",
            "keyword":"EquivalentCodeSequence",
            "value_representation":"SQ",
            "slug":"0008-0121"
        }
    }
    module_attr = [
        {
            "type":"3",
            "order":8,
            "module":"patient-study",
            "tag":"(0008,0121)",
            "description":"Codes that are considered equivalent by the creating system.\n\nOne or more Items are permitted in this Sequence.\n\nSee Section\u00a08.9.",
            "attribute":"0008-1084:0008-0121"
        },
        {
            "type":"3",
            "order":43,
            "module":"patient-study",
            "tag":"(0008,0121)",
            "description":"Codes that are considered equivalent by the creating system.\n\nOne or more Items are permitted in this Sequence.\n\nSee Section\u00a08.9.",
            "attribute":"0010-1021:0008-0121"
        }
    ]
    module = {
        "patient-study": {
            "name":"Patient Study",
            "link_to_standard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-4a"
        }
    }
    ciod_module = [
        {
            "information_entity":"Study",
            "module":"patient-study",
            "usage":"U",
            "conditional_statement":None,
            "ciod":"cr-image",
            "order":3
        }
    ]
    ciod = {
        "cr-image": {
            "description":"The Computed Radiography (CR) Image Information Object Definition specifies an image that has been created by a computed radiography imaging device.",
            "name":"CR Image",
            "link_to_standard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.2-1"
        }
    }
    assert attr['(0008,0121)'] == attributes['(0008,0121)']
    assert module_attr[0] in module_attribute_relationship
    assert module_attr[1] in module_attribute_relationship
    assert module['patient-study'] == modules['patient-study']
    assert ciod_module[0] in ciod_module_relationship
    assert ciod['cr-image'] == ciods['cr-image']

@pytest.mark.endtoend
def test_number_of_attribute_appearances(module_attribute_relationship, attributes):
    module_attr = [
        {
            "type": None,
            "order": 251,
            "module": "patient-demographic",
            "tag": "(0010,0213)",
            "description": "The nomenclature used for Strain Description (0010,0212). See Section\u00a0C.7.1.1.1.4.",
            "attribute": "0010-0213"
        },
        {
            "type": "3",
            "order": 288,
            "module": "patient",
            "tag": "(0010,0213)",
            "description": "The nomenclature used for Strain Description (0010,0212). See Section\u00a0C.7.1.1.1.4.",
            "attribute": "0010-0213"
        }
    ]

    attrs = {
        "(0010,0213)": {
            "name":"Strain Nomenclature",
            "retired":False,
            "value_multiplicity":"1",
            "keyword":"StrainNomenclature",
            "value_representation":"LO",
            "slug":"0010-0213"
        }
    }
    assert attrs['(0010,0213)'] == attributes['(0010,0213)']
    assert module_attr[0] in module_attribute_relationship
    assert module_attr[1] in module_attribute_relationship
    all_attribute_appearances = [rel for rel in module_attribute_relationship
                                 if rel['tag'] == '(0010,0213)']
    assert len(all_attribute_appearances) == 2

@pytest.mark.endtoend
def test_number_of_module_appearances(ciods, ciod_module_relationship, modules):
    module = {
        "volume-cropping": {
            "name":"Volume Cropping",
            "link_to_standard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.11.24-1"
        }
    }
    ciod_module = [
        {
            "information_entity":"Presentation State",
            "module":"volume-cropping",
            "usage":"U",
            "conditional_statement":None,
            "ciod":"planar-mpr-volumetric-presentation-state",
            "order":13
        }
    ]
    assert module['volume-cropping'] == modules['volume-cropping']
    assert ciod_module[0] in ciod_module_relationship
    all_module_appearances = [rel for rel in ciod_module_relationship
                              if rel['module'] == 'volume-cropping']
    assert len(all_module_appearances) == 1
