import subprocess

import pytest

import parse_lib as pl


@pytest.fixture(scope='module')
def make_standard():
    subprocess.run(['make', 'all'])


@pytest.fixture(scope='module')
def ciods(make_standard):
    return pl.read_json_to_dict('dist/ciods.json')


@pytest.fixture(scope='module')
def modules(make_standard):
    return pl.read_json_to_dict('dist/modules.json')


@pytest.fixture(scope='module')
def attributes(make_standard):
    return pl.read_json_to_dict('dist/attributes.json')


@pytest.fixture(scope='module')
def ciod_module_relationship(make_standard):
    return pl.read_json_to_dict('dist/ciod_to_modules.json')


@pytest.fixture(scope='module')
def module_attribute_relationship(make_standard):
    return pl.read_json_to_dict('dist/module_to_attributes.json')


@pytest.mark.endtoend
def test_total_number_ciods(ciods):
    defined_ciods = 122
    assert len(ciods) == defined_ciods


@pytest.mark.endtoend
def test_total_number_attributes(attributes):
    defined_valid_attributes = 4175
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
            "description": '<p>\n<a href="http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.7-1" target="_blank">Table\xa0A.7-1</a> specifies the Modules of the US Multi-frame Image IOD.</p>',
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.7-1",
            "name": "US Multi-frame Image",
            "id": "us-multi-frame-image",
        }
    }
    test_module = {
        "patient": {
            "name": "Patient",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-1",
            "id": "patient",
            "description":"<p>\n<a id=\"para_9dee1267-98f7-4fb1-bc67-aff85bef41a8\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.7-1\" shape=\"rect\" title=\"Table\u00a0C.7-1.\u00a0Patient Module Attributes\">Table\u00a0C.7-1</a> specifies the Attributes of the Patient that describe and identify the Patient who is the subject of a Study.\n            This Module contains Attributes of the patient that are needed for interpretation of the Composite Instances and are common for all studies performed on the patient. It contains Attributes that are also included in the Patient Modules in <a class=\"xref\" href=\"#sect_C.2\" shape=\"rect\" title=\"C.2\u00a0Patient Modules\">Section\u00a0C.2</a>.</p>"
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
            "module":"patient-study",
            "moduleDescription":"<p>\n<a id=\"para_9f0f6d2b-ece1-469b-bd8e-ed3e08db0e9b\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.7-4a\" shape=\"rect\" title=\"Table\u00a0C.7-4a.\u00a0Patient Study Module Attributes\">Table\u00a0C.7-4a</a> defines Attributes that provide information about the Patient at the time the Study started.</p>",
            "path":"patient-study:00081084:00080121",
            "tag":"(0008,0121)",
            "type":"3",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-4a",
            "description":"<td align=\"left\" colspan=\"1\" rowspan=\"1\">\n<p>\n<a id=\"para_c32b3ab1-f6a7-4c45-8594-14bcfea070f3\" shape=\"rect\"></a>Codes that are considered equivalent by the creating system.</p>\n<p>\n<a id=\"para_8d511d7c-f177-4d12-80c0-7f0d32653fdd\" shape=\"rect\"></a>One or more Items are permitted in this Sequence.</p>\n<p>\n<a id=\"para_4556c2fe-e657-43c7-8c66-b4603431e788\" shape=\"rect\"></a>See <span class=\"xref\" href=\"\" shape=\"rect\" title=\"8.9\u00a0Equivalent Code Sequence\">Section\u00a08.9</span>.</p>\n</td>",
            "externalReferences":[
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_8.9",
                    "title": "Section\u00a08.9"
                },
            ]
        },
        {
            "module":"patient-study",
            "moduleDescription":"<p>\n<a id=\"para_9f0f6d2b-ece1-469b-bd8e-ed3e08db0e9b\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.7-4a\" shape=\"rect\" title=\"Table\u00a0C.7-4a.\u00a0Patient Study Module Attributes\">Table\u00a0C.7-4a</a> defines Attributes that provide information about the Patient at the time the Study started.</p>",
            "path":"patient-study:00101021:00080121",
            "tag":"(0008,0121)",
            "type":"3",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-4a",
            "description":"<td align=\"left\" colspan=\"1\" rowspan=\"1\">\n<p>\n<a id=\"para_c32b3ab1-f6a7-4c45-8594-14bcfea070f3\" shape=\"rect\"></a>Codes that are considered equivalent by the creating system.</p>\n<p>\n<a id=\"para_8d511d7c-f177-4d12-80c0-7f0d32653fdd\" shape=\"rect\"></a>One or more Items are permitted in this Sequence.</p>\n<p>\n<a id=\"para_4556c2fe-e657-43c7-8c66-b4603431e788\" shape=\"rect\"></a>See <span class=\"xref\" href=\"\" shape=\"rect\" title=\"8.9\u00a0Equivalent Code Sequence\">Section\u00a08.9</span>.</p>\n</td>",
            "externalReferences":[
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_8.9",
                    "title": "Section\u00a08.9"
                },
            ]
        },
    ]
    module = {
        "patient-study":{
            "id":"patient-study",
            "name":"Patient Study",
            "description":"<p>\n<a id=\"para_9f0f6d2b-ece1-469b-bd8e-ed3e08db0e9b\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.7-4a\" shape=\"rect\" title=\"Table\u00a0C.7-4a.\u00a0Patient Study Module Attributes\">Table\u00a0C.7-4a</a> defines Attributes that provide information about the Patient at the time the Study started.</p>",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-4a"
        },
    }
    ciod_module = [
        {
            "ciod":"cr-image",
            "module":"patient-study",
            "usage":"U",
            "conditionalStatement": None,
            "informationEntity":"Study"
        },
    ]
    ciod = {
        "cr-image": {
            "description":"<p>\n<a href=\"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.2-1\" target=\"_blank\">Table\u00a0A.2-1</a> specifies the Modules of the CR Image IOD.</p>",
            "name":"CR Image",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_A.2-1",
            "id": "cr-image",
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
            "module":"patient-demographic",
            "moduleDescription":"<p>\n<a id=\"para_4a7adeab-f0e4-4bdb-a9b0-0c41212d1894\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.2-3\" shape=\"rect\" title=\"Table\u00a0C.2-3.\u00a0Patient Demographic Module Attributes\">Table\u00a0C.2-3</a> defines the Attributes relevant to generally describing a patient at a specific point in time, e.g., at the time of admission.</p>",
            "path":"patient-demographic:00100213",
            "tag":"(0010,0213)",
            "type":"None",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.2-3",
            "description":"<td align=\"left\" colspan=\"1\" rowspan=\"1\">\n<p>\n<a id=\"para_eb1a8550-fedf-4e1c-81bd-eeb6325f04b2\" shape=\"rect\"></a>The nomenclature used for Strain Description (0010,0212). See <span class=\"xref\" href=\"\" shape=\"rect\" title=\"C.7.1.1.1.4\u00a0Patient Strain and Genetic Modifications\">Section\u00a0C.7.1.1.1.4</span>.</p>\n</td>",
            "externalReferences":[
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.1.1.4",
                    "title": "Section\u00a0C.7.1.1.1.4"
                },
            ]
        },
        {
            "module":"patient",
            "moduleDescription":"<p>\n<a id=\"para_9dee1267-98f7-4fb1-bc67-aff85bef41a8\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.7-1\" shape=\"rect\" title=\"Table\u00a0C.7-1.\u00a0Patient Module Attributes\">Table\u00a0C.7-1</a> specifies the Attributes of the Patient that describe and identify the Patient who is the subject of a Study.\n            This Module contains Attributes of the patient that are needed for interpretation of the Composite Instances and are common for all studies performed on the patient. It contains Attributes that are also included in the Patient Modules in <a class=\"xref\" href=\"#sect_C.2\" shape=\"rect\" title=\"C.2\u00a0Patient Modules\">Section\u00a0C.2</a>.</p>",
            "path":"patient:00100213",
            "tag":"(0010,0213)",
            "type":"3",
            "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.7-1",
            "description":"<td align=\"left\" colspan=\"1\" rowspan=\"1\">\n<p>\n<a id=\"para_ea1c4023-3354-45aa-b770-e942796f32f3\" shape=\"rect\"></a>The nomenclature used for Strain Description (0010,0212). See <span class=\"xref\" href=\"\" shape=\"rect\" title=\"C.7.1.1.1.4\u00a0Patient Strain and Genetic Modifications\">Section\u00a0C.7.1.1.1.4</span>.</p>\n</td>",
            "externalReferences":[
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.1.1.1.4",
                    "title": "Section\u00a0C.7.1.1.1.4"
                },
            ]
        },
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
            "description":"<p>\n<a id=\"para_d9ae2959-d5cd-42dc-98d0-32b2a41d1fef\" shape=\"rect\"></a>\n<a class=\"xref\" href=\"#table_C.11.24-1\" shape=\"rect\" title=\"Table\u00a0C.11.24-1.\u00a0Volume Cropping Module Attributes\">Table\u00a0C.11.24-1</a> contains the attributes of the Volume Cropping Module. This Module limits the spatial extent of inputs in Volumetric Presentation State Input Sequence (0070,1201) that are used.</p>",
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
        }
    ]
    assert module['volume-cropping'] == modules['volume-cropping']
    assert ciod_module[0] in ciod_module_relationship
    all_module_appearances = [rel for rel in ciod_module_relationship
                              if rel['module'] == 'volume-cropping']
    assert len(all_module_appearances) == 1
