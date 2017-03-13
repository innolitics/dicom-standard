.SUFFIXES:

.PHONY: clean tests unittest endtoendtest updatestandard checkversions

PYTEST_BIN=python3 -m pytest


all: core_tables relationship_tables dist/references.json

core_tables: dist/ciods.json dist/modules.json dist/attributes.json

relationship_tables: dist/ciod_to_modules.json dist/module_to_attributes.json


dist/ciods.json: tmp/raw_ciod_module_tables.json
	python3 process_ciods.py $< $@

dist/ciod_to_modules.json: tmp/raw_ciod_module_tables.json
	python3 process_ciod_module_relationship.py $< $@

dist/modules.json: tmp/preprocessed_modules_attributes.json
	python3 process_modules.py $< $@

dist/module_to_attributes.json: tmp/modules_attributes_no_references.json tmp/raw_section_tables.json
	python3 postprocess_add_references.py $^ $@ dist/references.json

dist/attributes.json: tmp/PS3.6-cleaned.html extract_attributes.py
	python3 extract_attributes.py $< $@

dist/references.json: dist/module_to_attributes.json



tmp/modules_attributes_no_references.json: tmp/preprocessed_modules_attributes.json
	python3 process_module_attribute_relationship.py $< $@

tmp/preprocessed_modules_attributes.json: tmp/raw_module_attribute_tables.json tmp/raw_macro_tables.json
	python3 preprocess_modules_with_attributes.py $^ $@

tmp/raw_ciod_module_tables.json: tmp/PS3.3-cleaned.html extract_ciod_module_data.py
	python3 extract_ciod_module_data.py $< $@

tmp/raw_module_attribute_tables.json: tmp/PS3.3-cleaned.html extract_modules_with_attributes.py
	python3 extract_modules_with_attributes.py $< $@

tmp/raw_macro_tables.json: tmp/PS3.3-cleaned.html extract_macros.py
	python3 extract_macros.py $< $@

tmp/raw_section_tables.json: extract_sections.py tmp/PS3.3-cleaned.html tmp/PS3.4-cleaned.html \
                             tmp/PS3.6-cleaned.html tmp/PS3.15-cleaned.html tmp/PS3.16-cleaned.html \
                             tmp/PS3.17-cleaned.html tmp/PS3.18-cleaned.html
	python3 $^ $@



tmp/PS3.3-cleaned.html: PS3.3.html
	cat $< | sed -e 's/&nbps;/ /g' > $@

tmp/PS3.4-cleaned.html: PS3.4.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@

tmp/PS3.6-cleaned.html: PS3.6.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@

tmp/PS3.15-cleaned.html: PS3.15.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@

tmp/PS3.16-cleaned.html: PS3.16.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@

tmp/PS3.17-cleaned.html: PS3.17.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@

tmp/PS3.18-cleaned.html: PS3.18.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@


tests: unittest endtoendtest

unittest:
	$(PYTEST_BIN) -m 'not endtoend'

endtoendtest:
	$(PYTEST_BIN) -m 'endtoend'


updatestandard:
	if [ ! -d old_standards ]; then mkdir old_standards; fi
	mv PS3.* old_standards/
	wget http://dicom.nema.org/medical/dicom/current/output/html/part03.html -O PS3.3.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part04.html -O PS3.4.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part06.html -O PS3.6.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part15.html -O PS3.15.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part16.html -O PS3.16.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part17.html -O PS3.17.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part18.html -O PS3.18.html

checkversions:
	@python3 --version 2>&1 | grep -q 3.5. || { echo "Need Python 3.5" && exit 1; }

clean:
	git clean -fqx dist tmp
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
