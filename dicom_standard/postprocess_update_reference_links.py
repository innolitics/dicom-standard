import sys

from dicom_standard import parse_lib as pl


def update_sourceurls(pairs, references):
    ref_fragments = {url.split('#')[-1]: url for url in references.keys()}
    for pair in pairs:
        for ref in pair['externalReferences']:
            pair_fragment = ref['sourceUrl'].split('#')[-1]
            ref['sourceUrl'] = ref_fragments[pair_fragment]
    return pairs


if __name__ == '__main__':
    pairs = pl.read_json_data(sys.argv[1])
    references = pl.read_json_data(sys.argv[2])
    updated_pairs = update_sourceurls(pairs, references)
    pl.write_pretty_json(updated_pairs)
