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
        assert pair['path'].split(':')[-1] in attributes

@pytest.mark.endtoend
def test_vertical_samples_from_standard(ciods, modules, attributes):
    test_ciod = {
        "us-multi-frame-image": {
            "description": "The Ultrasound (US) Multi-frame Image Information Object Definition specifies a Multi-frame image that has been created by an ultrasound imaging device.",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.7-1",
            "name": "US Multi-frame Image",
            "id": "us-multi-frame-image",
            "order": 5
        }
    }
    test_module = {
        "patient": {
            "name": "Patient",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-1",
            "id": "patient"
        }
    }
    test_attribute = {
        "00100010": {
            "tag":"(0010,0010)",
            "retired": False,
            "keyword": "PatientName",
            "name": "Patient's Name",
            "valueMultiplicity": "1",
            "valueRepresentation": "PN"
        },
        "00080034": {
            "tag": "(0008,0034)",
            "retired": True,
            "keyword": "OverlayTime",
            "name": "Overlay Time",
            "valueMultiplicity": "1", 
            "valueRepresentation": "TM"
        },
        "00080108": {
            "tag": "(0008,0108)",
            "retired": False,
            "keyword": "ExtendedCodeMeaning",
            "name": "Extended Code Meaning",
            "valueMultiplicity": "1", 
            "valueRepresentation": "LT"
        }
    }
    assert test_ciod["us-multi-frame-image"] == ciods["us-multi-frame-image"] 
    assert test_module["patient"] == modules["patient"] 
    assert test_attribute["00100010"] == attributes["00100010"]
    assert test_attribute["00080034"] == attributes["00080034"]
    assert test_attribute["00080108"] == attributes["00080108"]

@pytest.mark.endtoend
def test_trace_from_attribute_to_ciod(ciods, ciod_module_relationship,
        modules, module_attribute_relationship, attributes):
    attr = {
        "00080121": {
            "name":"Equivalent Code Sequence",
            "retired": False,
            "valueMultiplicity":"1",
            "keyword":"EquivalentCodeSequence",
            "valueRepresentation":"SQ",
            "tag": "(0008,0121)"
        }
    }
    module_attr = [
        {
            "type":"3",
            "order":8,
            "depth": 1,
            "module":"patient-study",
            "tag":"(0008,0121)",
            "description":"Codes that are considered equivalent by the creating system.\n\nOne or more Items are permitted in this Sequence.\n\nSee Section\u00a08.9.",
            "path":"patient-study:00081084:00080121",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_8.8-1",
        },
        {
            "type":"3",
            "order":43,
            "depth": 1,
            "module":"patient-study",
            "tag":"(0008,0121)",
            "description":"Codes that are considered equivalent by the creating system.\n\nOne or more Items are permitted in this Sequence.\n\nSee Section\u00a08.9.",
            "path":"patient-study:00101021:00080121",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_8.8-1",
        }
    ]
    module = {
        "patient-study": {
            "name":"Patient Study",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-4a",
            "id": "patient-study"
        }
    }
    ciod_module = [
        {
            "informationEntity":"Study",
            "module":"patient-study",
            "usage":"U",
            "conditionalStatement":None,
            "ciod":"cr-image",
            "order":3
        }
    ]
    ciod = {
        "cr-image": {
            "description":"The Computed Radiography (CR) Image Information Object Definition specifies an image that has been created by a computed radiography imaging device.",
            "name":"CR Image",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.2-1",
            "id": "cr-image",
            "order": 0
        }
    }
    assert attr["00080121"] == attributes["00080121"]
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
            "depth": 0,
            "tag": "(0010,0213)",
            "description": "The nomenclature used for Strain Description (0010,0212). See Section\u00a0C.7.1.1.1.4.",
            "path": "patient-demographic:00100213",
            "linkToStandard": None
        },
        {
            "type": "3",
            "order": 288,
            "module": "patient",
            "depth": 0,
            "tag": "(0010,0213)",
            "description": "The nomenclature used for Strain Description (0010,0212). See Section\u00a0C.7.1.1.1.4.",
            "path": "patient:00100213",
            "linkToStandard": None
        }
    ]

    attrs = {
        "00100213": {
            "name":"Strain Nomenclature",
            "retired":False,
            "valueMultiplicity":"1",
            "keyword":"StrainNomenclature",
            "valueRepresentation":"LO",
            "tag": "(0010,0213)"
        }
    }
    assert attrs['00100213'] == attributes['00100213']
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
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.11.24-1",
            "id": "volume-cropping"
        }
    }
    ciod_module = [
        {
            "informationEntity":"Presentation State",
            "module":"volume-cropping",
            "usage":"U",
            "conditionalStatement":None,
            "ciod":"planar-mpr-volumetric-presentation-state",
            "order":13
        }
    ]
    assert module['volume-cropping'] == modules['volume-cropping']
    assert ciod_module[0] in ciod_module_relationship
    all_module_appearances = [rel for rel in ciod_module_relationship
                              if rel['module'] == 'volume-cropping']
    assert len(all_module_appearances) == 1
