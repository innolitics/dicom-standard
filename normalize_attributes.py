import sys

import parse_lib as pl


def extract_attributes(attribute_dict):
    attributes = {}
    for tag, attribute in attribute_dict.items():
        capital_tag = tag.upper()
        attributes[capital_tag] = attribute
        attributes[capital_tag]['slug'] = pl.create_slug(captial_tag)
    return attributes


if __name__ == "__main__":
    attribute_dict = pl.read_json_to_dict(sys.argv[1])
    attributes = extract_attributes(attribute_dict)
    pl.write_pretty_json(sys.argv[2], attributes)
