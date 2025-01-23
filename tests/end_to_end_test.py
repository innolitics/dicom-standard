import subprocess
from collections import Counter

import pytest

import dicom_standard.parse_lib as pl


@pytest.fixture(scope='module')
def make_standard():
    subprocess.run(['make', 'all'])


@pytest.fixture(scope='module')
def attributes(make_standard):
    return pl.read_json_data('standard/attributes.json')


@pytest.fixture(scope='module')
def ciods(make_standard):
    return pl.read_json_data('standard/ciods.json')


@pytest.fixture(scope='module')
def macros(make_standard):
    return pl.read_json_data('standard/macros.json')


@pytest.fixture(scope='module')
def modules(make_standard):
    return pl.read_json_data('standard/modules.json')


@pytest.fixture(scope='module')
def references(make_standard):
    return pl.read_json_data('standard/references.json')


@pytest.fixture(scope='module')
def sops(make_standard):
    return pl.read_json_data('standard/sops.json')


@pytest.fixture(scope='module')
def ciod_fg_macro_relationship(make_standard):
    return pl.read_json_data('standard/ciod_to_func_group_macros.json')


@pytest.fixture(scope='module')
def ciod_module_relationship(make_standard):
    return pl.read_json_data('standard/ciod_to_modules.json')


@pytest.fixture(scope='module')
def macro_attribute_relationship(make_standard):
    return pl.read_json_data('standard/macro_to_attributes.json')


@pytest.fixture(scope='module')
def module_attribute_relationship(make_standard):
    return pl.read_json_data('standard/module_to_attributes.json')


@pytest.fixture(scope='module')
def attribute_ids(attributes):
    return [d['id'] for d in attributes]


@pytest.fixture(scope='module')
def ciod_ids(ciods):
    return [d['id'] for d in ciods]


@pytest.fixture(scope='module')
def macro_ids(macros):
    return [d['id'] for d in macros]


@pytest.fixture(scope='module')
def module_ids(modules):
    return [d['id'] for d in modules]


@pytest.mark.endtoend
def test_valid_foreign_keys_ciod_macro(ciod_fg_macro_relationship, ciod_ids, macro_ids):
    for pair in ciod_fg_macro_relationship:
        assert pair['ciodId'] in ciod_ids
        assert pair['macroId'] in macro_ids


@pytest.mark.endtoend
def test_valid_foreign_keys_ciod_module(ciod_module_relationship, ciod_ids, module_ids):
    for pair in ciod_module_relationship:
        assert pair['ciodId'] in ciod_ids
        assert pair['moduleId'] in module_ids


@pytest.mark.endtoend
def test_valid_foreign_keys_macro_attribute(macro_attribute_relationship, macro_ids, attribute_ids):
    for pair in macro_attribute_relationship:
        assert pair['macroId'] in macro_ids
        assert pair['path'].split(':')[-1] in attribute_ids


@pytest.mark.endtoend
def test_valid_foreign_keys_module_attribute(module_attribute_relationship, module_ids, attribute_ids):
    for pair in module_attribute_relationship:
        assert pair['moduleId'] in module_ids
        assert pair['path'].split(':')[-1] in attribute_ids


@pytest.mark.endtoend
def test_macro_attr_refs_in_references(macro_attribute_relationship, references):
    for pair in macro_attribute_relationship:
        for ref in pair['externalReferences']:
            assert ref['sourceUrl'] in references


@pytest.mark.endtoend
def test_module_attr_refs_in_references(module_attribute_relationship, references):
    for pair in module_attribute_relationship:
        for ref in pair['externalReferences']:
            assert ref['sourceUrl'] in references


@pytest.mark.endtoend
def test_valid_ciod_names(sops, ciods):
    ciod_names = [d['name'] for d in ciods]
    for pair in sops:
        assert pair['ciod'] in ciod_names


@pytest.mark.endtoend
def test_vertical_samples_from_standard(ciods, modules, attributes):
    test_ciod = {
        "name":"Ultrasound Multi-frame Image",
        "id":"ultrasound-multi-frame-image",
        "description":"<p>\nThe <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.7.html#sect_A.7\" target=\"_blank\">Ultrasound Multi-frame Image IOD</a> specifies a Multi-frame Image that has been created by an ultrasound imaging device.</p>",
        "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.7.4.html#table_A.7-1"
    }
    test_module = {
        "name": "Patient",
        "id": "patient",
        "description": "<p>\n<span href=\"#table_C.7-1\">This module </span> specifies the Attributes of the <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1\" target=\"_blank\">Patient Module</a>, which identify and describe the Patient who is the subject of the Study. This Module contains Attributes of the Patient that are needed for interpretation of the Composite Instances and are common for all Studies performed on the Patient. It contains Attributes that are also included in the <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.2.html#sect_C.2\" target=\"_blank\">Section\u00a0C.2 Patient Modules</a>.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#table_C.7-1"
    }
    test_attributes = [
        {
            "tag": "(0010,0010)",
            "retired": 'N',
            "keyword": "PatientName",
            "name": "Patient's Name",
            "valueMultiplicity": "1",
            "valueRepresentation": "PN",
            "id": "00100010"
        },
        {
            "tag": "(0008,0034)",
            "retired": 'Y',
            "keyword": "OverlayTime",
            "name": "Overlay Time",
            "valueMultiplicity": "1",
            "valueRepresentation": "TM",
            "id": "00080034"
        },
        {
            "tag": "(0008,0108)",
            "retired": 'N',
            "keyword": "ExtendedCodeMeaning",
            "name": "Extended Code Meaning",
            "valueMultiplicity": "1",
            "valueRepresentation": "LT",
            "id": "00080108"
        }
    ]
    assert test_ciod in ciods
    assert test_module in modules
    assert all(attr in attributes for attr in test_attributes)


@pytest.mark.endtoend
def test_trace_from_ciod_to_func_group_attribute(ciod_fg_macro_relationship, ciod_ids, macro_ids,
                                                 macro_attribute_relationship, module_ids,
                                                 module_attribute_relationship, attributes):
    ciod_macro = {
        "ciodId": "enhanced-mr-image",
        "macroId": "referenced-image",
        "usage": "C",
        "conditionalStatement": "Required if the image or frame has been planned on another image or frame. May be present otherwise",
        "moduleType": "Multi-frame"
    }
    macro_attr = {
        "macroId": "referenced-image",
        "path": "referenced-image:00081140:00081150",
        "tag": "(0008,1150)",
        "type": "1",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.16.2.html#table_C.7.6.16-6",
        "description": "<p>\nUniquely identifies the referenced SOP Class.</p>",
        "externalReferences": []
    }
    ciod_specific_module_id = f'{ciod_macro["ciodId"]}-multi-frame-functional-groups'
    module_attr = {
        "moduleId": "enhanced-mr-image-multi-frame-functional-groups",
        "path": "enhanced-mr-image-multi-frame-functional-groups:52009230:00081140:00081150",
        "tag": "(0008,1150)",
        "type": "1",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.16.2.html#table_C.7.6.16-6",
        "description": "<p>\nUniquely identifies the referenced SOP Class.</p><h3>Note</h3><p>Part of the Referenced Image Functional Group Macro with usage: C</p><p>Required if the image or frame has been planned on another image or frame. May be present otherwise.</p>",
        "externalReferences": []
    }
    attr = {
        "tag": "(0008,1150)",
        "name": "Referenced SOP Class UID",
        "keyword": "ReferencedSOPClassUID",
        "valueRepresentation": "UI",
        "valueMultiplicity": "1",
        "retired": "N",
        "id": "00081150"
    }
    assert ciod_macro in ciod_fg_macro_relationship
    assert ciod_macro['ciodId'] in ciod_ids
    assert ciod_macro['macroId'] in macro_ids
    assert macro_attr in macro_attribute_relationship
    assert ciod_specific_module_id in module_ids
    assert module_attr in module_attribute_relationship
    assert attr in attributes


@pytest.mark.endtoend
def test_trace_from_attribute_to_ciod(ciods, ciod_module_relationship, modules,
                                      module_attribute_relationship, attributes):
    attr = {
        "name": "Equivalent Code Sequence",
        "retired": 'N',
        "valueMultiplicity": "1",
        "keyword": "EquivalentCodeSequence",
        "valueRepresentation": "SQ",
        "tag": "(0008,0121)",
        "id": "00080121"
    }
    module_attr = [
        {
            "moduleId": "patient-study",
            "path": "patient-study:00081084:00080121",
            "tag": "(0008,0121)",
            "type": "3",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a",
            "description": "<p>\nCodes that are considered equivalent by the creating system.</p>\n<p>\nOne or more Items are permitted in this Sequence.</p>\n<p>\nSee <span href=\"\">Section\u00a08.9</span>.</p>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_8.9.html#sect_8.9",
                    "title": "Section\u00a08.9"
                },
            ]
        },
        {
            "moduleId": "patient-study",
            "path": "patient-study:00101021:00080121",
            "tag": "(0008,0121)",
            "type": "3",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a",
            "description": "<p>\nCodes that are considered equivalent by the creating system.</p>\n<p>\nOne or more Items are permitted in this Sequence.</p>\n<p>\nSee <span href=\"\">Section\u00a08.9</span>.</p>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_8.9.html#sect_8.9",
                    "title": "Section\u00a08.9"
                },
            ]
        },
    ]
    module = {
        "id": "patient-study",
        "name": "Patient Study",
        "description": "<p>\n<span href=\"#table_C.7-4a\">This module </span> specifies the Attributes of the <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#sect_C.7.2.2\" target=\"_blank\">Patient Study Module</a>, which provide information about the Patient at the time the Study started.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a"
    }
    ciod_module = {
        "ciodId": "computed-radiography-image",
        "moduleId": "patient-study",
        "usage": "U",
        "conditionalStatement": None,
        "informationEntity": "Study"
    }
    ciod = {
        "name":"Computed Radiography Image",
        "id":"computed-radiography-image",
        "description":"<p>\nThe <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.2.html#sect_A.2\" target=\"_blank\">Computed Radiography Image IOD</a> specifies an image that has been created by a computed radiography imaging device.</p>",
        "linkToStandard":"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.2.3.html#table_A.2-1"
    }
    assert attr in attributes
    assert module_attr[0] in module_attribute_relationship
    assert module_attr[1] in module_attribute_relationship
    assert module in modules
    assert ciod_module in ciod_module_relationship
    assert ciod in ciods


@pytest.mark.endtoend
def test_number_of_attribute_appearances(module_attribute_relationship, attributes):
    attr = {
        "name": "Strain Nomenclature",
        "retired": 'N',
        "valueMultiplicity": "1",
        "keyword": "StrainNomenclature",
        "valueRepresentation": "LO",
        "tag": "(0010,0213)",
        "id": "00100213"
    }
    module_attr = [
        {
            "moduleId": "patient-demographic",
            "path": "patient-demographic:00100213",
            "tag": "(0010,0213)",
            "type": "None",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.2.3.html#table_C.2-3",
            "description": "<p>\nThe nomenclature used for Strain Description (0010,0212). See <span href=\"\">Section\u00a0C.7.1.1.1.4</span>.</p>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1.1.4",
                    "title": "Section\u00a0C.7.1.1.1.4"
                },
            ]
        },
        {
            "moduleId": "patient",
            "path": "patient:00100213",
            "tag": "(0010,0213)",
            "type": "3",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#table_C.7-1",
            "description": "<p>\nThe nomenclature used for Strain Description (0010,0212). See <span href=\"\">Section\u00a0C.7.1.1.1.4</span>.</p>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1.1.4",
                    "title": "Section\u00a0C.7.1.1.1.4"
                },
            ]
        },
    ]
    assert attr in attributes
    assert module_attr[0] in module_attribute_relationship
    assert module_attr[1] in module_attribute_relationship
    all_attribute_appearances = [rel for rel in module_attribute_relationship
                                 if rel['tag'] == attr['tag']]
    assert len(all_attribute_appearances) == 2


@pytest.mark.endtoend
def test_number_of_module_appearances(ciod_module_relationship, modules):
    module = {
        "name": "Volume Cropping",
        "id": "volume-cropping",
        "description": "<p>\n<span href=\"#table_C.11.24-1\">This module </span> specifies the Attributes of the <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.11.24.html#sect_C.11.24\" target=\"_blank\">Volume Cropping Module</a>. This Module limits the spatial extent of inputs in Volumetric Presentation State Input Sequence (0070,1201) that are used.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.11.24.html#table_C.11.24-1"
    }
    ciod_module = [
        {
            "ciodId": "planar-mpr-volumetric-presentation-state",
            "moduleId": "volume-cropping",
            "usage": "C",
            "conditionalStatement": "Required if Global Crop (0070,120B) or any value of Crop (0070,1204) is YES",
            "informationEntity": "Presentation State"
        },
        {
            "ciodId": "volume-rendering-volumetric-presentation-state",
            "moduleId": "volume-cropping",
            "usage": "C",
            "conditionalStatement": "Required if Global Crop (0070,120B) or any value of Crop (0070,1204) is YES",
            "informationEntity": "Presentation State"
        },
    ]
    assert module in modules
    for ciod_module_pair in ciod_module:
        assert ciod_module_pair in ciod_module_relationship
    all_module_appearances = [rel for rel in ciod_module_relationship
                              if rel['moduleId'] == module['id']]
    assert len(all_module_appearances) == 2


@pytest.mark.endtoend
class TestUniqueIds:
    def get_duplicates(self, lst):
        return [k for k, v in Counter(lst).items() if v > 1]

    def get_duplicate_paths(self, dict_list):
        path_list = [d['path'] for d in dict_list]
        return self.get_duplicates(path_list)

    def test_no_duplicate_attributes(self, attribute_ids):
        assert not self.get_duplicates(attribute_ids)

    def test_no_duplicate_ciods(self, ciod_ids):
        assert not self.get_duplicates(ciod_ids)

    def test_no_duplicate_macros(self, macro_ids):
        assert not self.get_duplicates(macro_ids)

    def test_no_duplicate_modules(self, module_ids):
        assert not self.get_duplicates(module_ids)

    def test_no_duplicate_sops(self, sops):
        sop_ids = [d['id'] for d in sops]
        assert not self.get_duplicates(sop_ids)

    def test_no_duplicate_ciod_module_relationships(self, ciod_module_relationship):
        key_list = [d['ciodId'] + d['moduleId'] for d in ciod_module_relationship]
        assert not self.get_duplicates(key_list)

    def test_no_duplicate_ciod_macro_relationships(self, ciod_fg_macro_relationship):
        key_list = [d['ciodId'] + d['macroId'] for d in ciod_fg_macro_relationship]
        assert not self.get_duplicates(key_list)

    def test_no_duplicate_macro_attr_paths(self, macro_attribute_relationship):
        assert not self.get_duplicate_paths(macro_attribute_relationship)

    def test_no_duplicate_module_attr_paths(self, module_attribute_relationship):
        assert not self.get_duplicate_paths(module_attribute_relationship)
