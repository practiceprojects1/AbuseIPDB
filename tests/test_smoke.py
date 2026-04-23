"""
Smoke tests for data processing logic used in abipdbIOCS.py.
These run without hitting the AbuseIPDB API.
"""
import pandas as pd


SAMPLE_DATA = [
    {
        "ipAddress": "1.2.3.4",
        "abuseConfidenceScore": 90,
        "countryCode": "US",
        "lastReportedAt": "2024-01-01T00:00:00+00:00",
    },
    {
        "ipAddress": "5.6.7.8",
        "abuseConfidenceScore": 85,
        "countryCode": "MX",
        "lastReportedAt": "2024-01-02T00:00:00+00:00",
    },
    # duplicate of first entry
    {
        "ipAddress": "1.2.3.4",
        "abuseConfidenceScore": 90,
        "countryCode": "US",
        "lastReportedAt": "2024-01-01T00:00:00+00:00",
    },
]

SELECTED_COLUMNS = [
    "abuseConfidenceScore",
    "countryCode",
    "ipAddress",
    "lastReportedAt",
]


def test_imports():
    import requests  # noqa: F401
    import pandas  # noqa: F401
    import json  # noqa: F401
    import csv  # noqa: F401


def test_json_normalize_produces_expected_columns():
    df = pd.json_normalize(SAMPLE_DATA)
    for col in SELECTED_COLUMNS:
        assert col in df.columns, f"Expected column '{col}' not found"


def test_column_selection():
    df = pd.json_normalize(SAMPLE_DATA)
    df_selected = df[SELECTED_COLUMNS]
    assert list(df_selected.columns) == SELECTED_COLUMNS
    assert len(df_selected) == len(SAMPLE_DATA)


def test_deduplication():
    df = pd.json_normalize(SAMPLE_DATA)
    deduped = df.drop_duplicates()
    assert len(deduped) == 2, f"Expected 2 unique rows, got {len(deduped)}"


def test_confidence_score_range():
    df = pd.json_normalize(SAMPLE_DATA)
    assert df["abuseConfidenceScore"].between(0, 100).all()
