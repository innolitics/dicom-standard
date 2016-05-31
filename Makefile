all: parser.py PS3.3.html
	cp PS3.3.html temp_standard.html
	sed -i -e 's/&nbps;/ /g' temp_standard.html
	rm -f temp_standard.html-e
	python parser.py > ciod_modules.json
	rm -f temp_standard.html

clean: 
	rm -f ciod_modules.json 
