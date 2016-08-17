import json

from parse_lib import create_slug, read_json_to_dict

SITEMAP_INDEX_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
SITEMAP_INDEX_FOOTER = '</sitemapindex>\n'
BASE_URL = "dicom.innolitics.com/ciods"

def main():
    ciods = read_json_to_dict('./dist/ciods.json')
    ciod_modules = read_json_to_dict('./dist/ciod_to_modules.json')
    module_attributes = read_json_to_dict('./dist/module_to_attributes.json')

    with open("./sitemap/sitemapindex.xml", "w") as sm_index:
        sm_index.write(SITEMAP_INDEX_HEADER)
        for slug in ciods.keys():
            sm_index.write(sitemap_index_entry(slug))
            with open("./sitemap/"+slug+".sitemap.txt", "w") as sitemap:
                sitemap.write(BASE_URL + "/" + slug + "\n")
                for rel in ciod_modules:
                    if rel["ciod"] == slug:
                        sitemap.write(BASE_URL + "/" + slug + "/" + rel["module"] + "\n")
                        for pair in module_attributes:
                            if pair["module"] == rel["module"]:
                                sitemap.write(BASE_URL + "/" + slug + "/" + pretty_print_path(pair["path"]) + "\n")
        sm_index.write(SITEMAP_INDEX_FOOTER)

def sitemap_index_entry(slug):
    return "<sitemap><loc>dicom.innolitics.com/sitemaps/"+slug+".sitemap.txt</loc></sitemap>\n"

def pretty_print_path(path):
    newpath = path.replace(":", "/")
    return newpath

if __name__ == "__main__":
    main()
