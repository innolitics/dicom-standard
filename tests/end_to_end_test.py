import subprocess
from collections import Counter
from operator import itemgetter

import pytest

import dicom_standard.parse_lib as pl


@pytest.fixture(scope='module')
def make_standard():
    subprocess.run(['make', 'all'])


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
def attributes(make_standard):
    return pl.read_json_data('standard/attributes.json')


@pytest.fixture(scope='module')
def sops(make_standard):
    return pl.read_json_data('standard/sops.json')


@pytest.fixture(scope='module')
def references(make_standard):
    return pl.read_json_data('standard/references.json')


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


@pytest.mark.endtoend
def test_valid_foreign_keys_ciod_macro(ciod_fg_macro_relationship, ciods, macros):
    for pair in ciod_fg_macro_relationship:
        assert any(d['id'] == pair['ciodId'] for d in ciods)
        assert any(d['id'] == pair['macroId'] for d in macros)


@pytest.mark.endtoend
def test_valid_foreign_keys_ciod_module(ciod_module_relationship, ciods, modules):
    for pair in ciod_module_relationship:
        assert any(d['id'] == pair['ciodId'] for d in ciods)
        assert any(d['id'] == pair['moduleId'] for d in modules)


@pytest.mark.endtoend
def test_valid_foreign_keys_macro_attribute(macro_attribute_relationship, macros, attributes):
    for pair in macro_attribute_relationship:
        assert any(d['id'] == pair['macroId'] for d in macros)
        assert any(d['id'] == pair['path'].split(':')[-1] for d in attributes)


@pytest.mark.endtoend
def test_valid_foreign_keys_module_attribute(module_attribute_relationship, modules, attributes):
    for pair in module_attribute_relationship:
        assert any(d['id'] == pair['moduleId'] for d in modules)
        assert any(d['id'] == pair['path'].split(':')[-1] for d in attributes)


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
    for pair in sops:
        assert any(d['name'] == pair['ciod'] for d in ciods)


@pytest.mark.endtoend
def test_vertical_samples_from_standard(ciods, modules, attributes):
    test_ciod = {
        "name": "US Multi-frame Image",
        "id": "us-multi-frame-image",
        "description": "<p>\nThe Ultrasound (US) Multi-frame Image Information Object Definition specifies a Multi-frame image that has been created by an ultrasound imaging device.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.7.4.html#table_A.7-1",
    }
    test_module = {
        "name": "Patient",
        "id": "patient",
        "description": "<p>\n<span href=\"#table_C.7-1\">This module </span> specifies the Attributes of the Patient that describe and identify the Patient who is the subject of a Study. This Module contains Attributes of the Patient that are needed for interpretation of the Composite Instances and are common for all Studies performed on the Patient. It contains Attributes that are also included in the Patient Modules in <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.2.html#sect_C.2\" target=\"_blank\">Section\u00a0C.2</a>.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#table_C.7-1",
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
def test_trace_from_ciod_to_func_group_attribute(ciod_fg_macro_relationship, ciods, macros,
                                                 macro_attribute_relationship, modules,
                                                 module_attribute_relationship, attributes):
    ciod_macro = {
        "ciodId": "enhanced-mr-image",
        "macroId": "referenced-image",
        "usage": "C",
        "conditionalStatement": "Required if the image or frame has been planned on another image or frame. May be present otherwise"
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
    assert ciod_macro['ciodId'] in map(itemgetter('id'), ciods)
    assert ciod_macro['macroId'] in map(itemgetter('id'), macros)
    assert macro_attr in macro_attribute_relationship
    assert ciod_specific_module_id in map(itemgetter('id'), modules)
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
        "description": "<p>\n<span href=\"#table_C.7-4a\">This module </span> defines Attributes that provide information about the Patient at the time the Study started.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a",
    }
    ciod_module = {
        "ciodId": "cr-image",
        "moduleId": "patient-study",
        "usage": "U",
        "conditionalStatement": None,
        "informationEntity": "Study"
    }
    ciod = {
        "name": "CR Image",
        "id": "cr-image",
        "description": "<p>\nThe Computed Radiography (CR) Image Information Object Definition specifies an image that has been created by a computed radiography imaging device.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.2.3.html#table_A.2-1",
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
def test_number_of_module_appearances(ciods, ciod_module_relationship, modules):
    module = {
        "name": "Volume Cropping",
        "id": "volume-cropping",
        "description": "<p>\n<span href=\"#table_C.11.24-1\">This module </span> contains the Attributes of the Volume Cropping Module. This Module limits the spatial extent of inputs in Volumetric Presentation State Input Sequence (0070,1201) that are used.</p>",
        "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.11.24.html#table_C.11.24-1",
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
    def get_duplicates(self, l):
        return [k for k, v in Counter(l).items() if v > 1]

    def get_duplicate_ids(self, dict_list):
        id_list = [d['id'] for d in dict_list]
        return self.get_duplicates(id_list)

    def get_duplicate_paths(self, dict_list):
        path_list = [d['path'] for d in dict_list]
        return self.get_duplicates(path_list)

    def test_no_duplicate_attributes(self, attributes):
        assert not self.get_duplicate_ids(attributes)

    def test_no_duplicate_ciods(self, ciods):
        assert not self.get_duplicate_ids(ciods)

    def test_no_duplicate_macros(self, macros):
        assert not self.get_duplicate_ids(macros)

    def test_no_duplicate_modules(self, modules):
        assert not self.get_duplicate_ids(modules)

    def test_no_duplicate_sops(self, sops):
        assert not self.get_duplicate_ids(sops)

    def test_no_duplicate_macro_attr_paths(self, macro_attribute_relationship):
        assert not self.get_duplicate_paths(macro_attribute_relationship)

    def test_no_duplicate_module_attr_paths(self, module_attribute_relationship):
        assert not self.get_duplicate_paths(module_attribute_relationship)

    def test_no_duplicate_ciod_module_relationships(self, ciod_module_relationship):
        key_list = [d['ciodId'] + d['moduleId'] for d in ciod_module_relationship]
        assert not self.get_duplicates(key_list)

    def test_no_duplicate_ciod_macro_relationships(self, ciod_fg_macro_relationship):
        key_list = [d['ciodId'] + d['macroId'] for d in ciod_fg_macro_relationship]
        assert not self.get_duplicates(key_list)
