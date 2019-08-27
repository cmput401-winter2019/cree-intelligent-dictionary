import pytest

from DatabaseManager.xml_consistency_checker import parse_xml_lc
from constants import LexicalCategory


@pytest.mark.parametrize(
    ("lc_string", "expected_ic_obj"),
    [
        ("NDA-1", LexicalCategory.NAD),
        ("NDI-?", LexicalCategory.NID),
        ("NA-3", LexicalCategory.NA),
        ("NA-4w", LexicalCategory.NA),
        ("NDA-2", LexicalCategory.NAD),
        ("VTI-2", LexicalCategory.VTI),
        ("NDI-3", LexicalCategory.NID),
        ("NDI-x", LexicalCategory.NID),
        ("NDA-x", LexicalCategory.NAD),
        ("IPJ  Exclamation", None),
        ("NI-5", LexicalCategory.NI),
        ("NDA-4", LexicalCategory.NAD),
        ("VII-n", LexicalCategory.VII),
        ("NDI-4", LexicalCategory.NID),
        ("VTA-2", LexicalCategory.VTA),
        ("IPH", None),
        ("IPC ;; IPJ", LexicalCategory.IPC),
        ("VAI-v", LexicalCategory.VAI),
        ("VTA-1", LexicalCategory.VTA),
        ("NI-3", LexicalCategory.NI),
        ("VAI-n", LexicalCategory.VAI),
        ("NDA-4w", LexicalCategory.NAD),
        ("IPJ", None),
        ("PrI", None),
        ("NA-2", LexicalCategory.NA),
        ("IPN", None),
        ("PR", None),
        ("IPV", None),
        ("NA-?", LexicalCategory.NA),
        ("NI-1", LexicalCategory.NI),
        ("VTA-3", LexicalCategory.VTA),
        ("NI-?", LexicalCategory.NI),
        ("VTA-4", LexicalCategory.VTA),
        ("VTI-3", LexicalCategory.VTI),
        ("NI-2", LexicalCategory.NI),
        ("NA-4", LexicalCategory.NA),
        ("NDI-1", LexicalCategory.NID),
        ("NA-1", LexicalCategory.NA),
        ("IPP", None),
        ("NI-4w", LexicalCategory.NI),
        ("INM", None),
        ("VTA-5", LexicalCategory.VTA),
        ("PrA", None),
        ("NDI-2", LexicalCategory.NID),
        ("IPC", LexicalCategory.IPC),
        ("VTI-1", LexicalCategory.VTI),
        ("NI-4", LexicalCategory.NI),
        ("NDA-3", LexicalCategory.NAD),
        ("VII-v", LexicalCategory.VII),
        ("Interr", None),
    ],
)
def test_parse_xml_lc(lc_string, expected_ic_obj):
    assert parse_xml_lc(lc_string) == expected_ic_obj
