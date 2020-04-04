import sys

from dicom_standard import parse_lib as pl


def update_sourceurls(module_attr_pairs, references):
    for pair in module_attr_pairs:
        for ref in pair['externalReferences']:
            for source_url in references.keys():
                reference_fragment = source_url.split('#')[-1]
                pair_fragment = ref['sourceUrl'].split('#')[-1]
                if pair_fragment == reference_fragment:
                    ref['sourceUrl'] = source_url
                    break
    return module_attr_pairs


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_data(sys.argv[1])
    references = pl.read_json_data(sys.argv[2])
    updated_pairs = update_sourceurls(module_attr_pairs, references)
    pl.write_pretty_json(updated_pairs)
