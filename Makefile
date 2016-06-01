all: tmp/PS3.3-space-expand.html parser.py
	python parser.py tmp/PS3.3-space-expand.html

tmp/PS3.3-space-expand.html: PS3.3.html
	cat $< | sed -e 's/&nbps;/ /g' > $@

clean: 
	rm -f parser.pyc tmp/*

install:
	pip install -r requirements.txt
