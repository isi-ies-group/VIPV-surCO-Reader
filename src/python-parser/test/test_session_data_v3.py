from surco_parser import SessionDataV3

import pandas as pd
import pytest
import zoneinfo

from conftest import TEST_DATA_DIR


@pytest.fixture
def session_v3_file():
    return TEST_DATA_DIR / "v3.txt"


def test_SessionDataV3(session_v3_file):
    session = SessionDataV3.from_file(session_v3_file)
    assert session.start_localized_instant == pd.Timestamp(
        "2025-03-06T11:15:21.569Z"
    )
    assert session.timezone == zoneinfo.ZoneInfo("Atlantic/Canary")
