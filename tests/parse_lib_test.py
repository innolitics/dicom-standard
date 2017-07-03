import dicom_standard.parse_lib as pl


def test_create_slug():
    test_titles = [
        "Example (1)",
        "I'm try'n (sorta) to    test",
        "(Sample/Test/Evaluate)"
    ]
    expected_result = [
        "example-1",
        "im-tryn-sorta-to-test",
        "sample-test-evaluate"
    ]
    assert list(map(pl.create_slug, test_titles)) == expected_result
