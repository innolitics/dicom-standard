from typing import cast, List
import sys

from dicom_standard import parse_lib as pl
from dicom_standard.macro_utils import MetadataTableType
from dicom_standard.preprocess_modules_with_attributes import (
    key_tables_by_id,
    expand_all_macros,
    preprocess_attribute_fields,
    expand_hierarchy,
)


if __name__ == '__main__':
    module_macro_attr_tables = cast(List[MetadataTableType], pl.read_json_data(sys.argv[1]))
    id_to_table = key_tables_by_id(module_macro_attr_tables)
    macro_attr_tables = [table for table in module_macro_attr_tables if table['isMacro']]
    expanded_tables = expand_all_macros(macro_attr_tables, id_to_table)
    preprocessed_tables = preprocess_attribute_fields(expanded_tables)
    tables_with_hierarchy = expand_hierarchy(preprocessed_tables)
    pl.write_pretty_json(tables_with_hierarchy)
