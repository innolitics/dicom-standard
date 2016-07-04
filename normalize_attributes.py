import sys

import parse_lib as pl


def extract_attributes(modules_with_attributes):
    attributes = {}
    for module in modules_with_attributes:
        for attribute in module['data']:
            tag = attribute['tag']
            attributes[tag] = attribute
            attributes[tag]['slug'] = pl.create_slug(tag)
    return attributes


if __name__ == "__main__":
    modules_with_attributes = pl.read_json_to_dict(sys.argv[1])
    attributes = extract_attributes(modules_with_attributes)
    pl.write_pretty_json(sys.argv[2], attributes)
