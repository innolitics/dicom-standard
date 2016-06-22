import sys

import parse.parse_lib as pl

def normalize_modules_attributes(input_json_path, modules_output_path, attributes_output_path):
    module_attr_list = pl.read_json_to_dict(input_json_path) 

if __name__ == "__main__":
    normalize_modules_attributes(sys.argv[1], sys.argv[2], sys.argv[3])
