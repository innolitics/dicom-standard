.SUFFIXES:

PYTEST_BIN=python3 -m pytest


all: core_tables relationship_tables sitemaps


core_tables: dist/ciods.json dist/modules.json dist/attributes.json

relationship_tables: dist/ciod_to_modules.json dist/module_to_attributes.json

sitemaps:
	python3 generate_sitemaps.py

dist/ciod_to_modules.json: tmp/ciods_with_modules.json
	python3 normalize_ciod_module_relationship.py $< $@

dist/module_to_attributes.json: tmp/modules_with_attributes.json
	python3 normalize_module_attr_relationship.py $< $@


dist/ciods.json: tmp/ciods_with_modules.json
	python3 normalize_ciods.py $< $@

dist/modules.json: tmp/modules_with_attributes.json
	python3 normalize_modules.py $< $@


dist/attributes.json: tmp/PS3.6-cleaned.html extract_data_element_registry.py
	python3 extract_data_element_registry.py $< $@

tmp/ciods_with_modules.json: tmp/PS3.3-cleaned.html extract_ciods_with_modules.py
	python3 extract_ciods_with_modules.py $< $@

tmp/extra_referenced_sections.json: tmp/modules_with_attributes.json tmp/PS3.3-cleaned.html
	python3 parse_extra_sections.py $@ $^

tmp/modules_with_attributes.json: tmp/modules_with_raw_attributes.json process_modules_with_attributes.py
	python3 process_modules_with_attributes.py $< $@

tmp/modules_with_raw_attributes.json: tmp/PS3.3-cleaned.html extract_modules_with_attributes.py
	python3 extract_modules_with_attributes.py $< $@


tmp/PS3.3-cleaned.html: PS3.3.html
	cat $< | sed -e 's/&nbps;/ /g' > $@

tmp/PS3.6-cleaned.html: PS3.6.html
	cat $< | sed -e 's/&nbps;/ /g' -e 's/​//g' > $@


tests: unittest endtoendtest

unittest:
	$(PYTEST_BIN) -m 'not endtoend'

endtoendtest:
	$(PYTEST_BIN) -m 'endtoend'


updatestandard:
	wget http://dicom.nema.org/medical/dicom/current/output/html/part03.html -O PS3.3.html
	wget http://dicom.nema.org/medical/dicom/current/output/html/part06.html -O PS3.6.html


clean:
	rm -f *.pyc tmp/* dist/* tests/*.pyc tests/*.pyc
