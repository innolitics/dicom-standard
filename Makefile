all: parser.py PS3.3.html
	cp PS3.3.html temp_standard.html
	sed -i -e 's/&nbps;/ /g' temp_standard.html
	rm -f temp_standard.html-e
	python parser.py
	rm -f temp_standard.html

clean: 
	rm -f ciod_module_rough.json module_attr_rough.json parser.pyc requirements.txt

install:
	pip freeze > requirements.txt
	pip install -r requirements.txt
