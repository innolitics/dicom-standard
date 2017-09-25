.SUFFIXES:)

.PHONY: clean tests unittest endtoendtest updatestandard checkversions

PYTEST_BIN=python3 -m pytest

PYTHONPATH_PREFIX=PYTHONPATH=..

cleaned_dicom_html=$(patsubst standard/%.html,tmp/%.html,$(wildcard standard/*.html))


all: core_tables relationship_tables dist/references.json

core_tables: dist/ciods.json dist/modules.json dist/attributes.json

relationship_tables: dist/ciod_to_modules.json dist/module_to_attributes.json


dist/ciods.json: tmp/raw_ciod_module_tables.json
	$(PYTHONPATH_PREFIX) python3 process_ciods.py $< > $@

dist/ciod_to_modules.json: tmp/raw_ciod_module_tables.json
	$(PYTHONPATH_PREFIX) python3 process_ciod_module_relationship.py $< > $@

dist/modules.json: tmp/preprocessed_modules_attributes.json
	$(PYTHONPATH_PREFIX) python3 process_modules.py $< > $@

dist/module_to_attributes.json: tmp/modules_attributes_partial_references.json dist/references.json
	$(PYTHONPATH_PREFIX) python3 postprocess_update_reference_links.py $^ > $@

dist/attributes.json: tmp/part06.html extract_attributes.py
	$(PYTHONPATH_PREFIX) python3 extract_attributes.py $< > $@

dist/references.json: tmp/modules_attributes_partial_references.json tmp/raw_section_tables.json
	$(PYTHONPATH_PREFIX) python3 postprocess_save_references.py $^ > $@


tmp/modules_attributes_partial_references.json: tmp/modules_attributes_no_references.json
	$(PYTHONPATH_PREFIX) python3 postprocess_mark_references.py $< > $@

tmp/modules_attributes_no_references.json: tmp/preprocessed_modules_attributes.json
	$(PYTHONPATH_PREFIX) python3 process_module_attribute_relationship.py $< > $@

tmp/preprocessed_modules_attributes.json: tmp/raw_module_attribute_tables.json tmp/raw_macro_tables.json
	$(PYTHONPATH_PREFIX) python3 preprocess_modules_with_attributes.py $^ > $@

tmp/raw_ciod_module_tables.json: tmp/part03.html extract_ciod_module_data.py
	$(PYTHONPATH_PREFIX) python3 extract_ciod_module_data.py $< > $@

tmp/raw_module_attribute_tables.json: tmp/part03.html extract_modules_with_attributes.py
	$(PYTHONPATH_PREFIX) python3 extract_modules_with_attributes.py $< > $@

tmp/raw_macro_tables.json: tmp/part03.html extract_macros.py
	$(PYTHONPATH_PREFIX) python3 extract_macros.py $< > $@

tmp/raw_section_tables.json: extract_sections.py $(cleaned_dicom_html)
	$(PYTHONPATH_PREFIX) python3 $^ > $@


tmp/%.html: standard/%.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@


tests: unittest endtoendtest

unittest:
	$(PYTEST_BIN) -m 'not endtoend'

endtoendtest:
	$(PYTEST_BIN) -m 'endtoend'


updatestandard:
	if [ ! -d old_standards ]; then mkdir old_standards; fi
	mv -f standard/*.html old_standards/
	wget http://dicom.nema.org/medical/dicom/current/output/html/part03.html -O standard/part03.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part04.html -O standard/part04.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part06.html -O standard/part06.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part15.html -O standard/part15.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part16.html -O standard/part16.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part17.html -O standard/part17.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part18.html -O standard/part18.html

checkversions:
	@python3 --version 2>&1 | grep -q 3.5. || { echo "Need Python 3.5" && exit 1; }

clean:
	git clean -fqx dist tmp .
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
