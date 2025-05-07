from surco_parser import SessionDataV4
from surco_parser import SessionFactory

import pandas as pd
import pytest
import zoneinfo

from conftest import TEST_DATA_DIR


@pytest.fixture
def session_v4_file():
    return TEST_DATA_DIR / "v4.txt"


def test_SessionDataV4(session_v4_file):
    session = SessionDataV4.from_file(session_v4_file)
    assert session.start_localized_instant == pd.Timestamp(
        "2025-04-25T09:37:43.382428Z"
    )
    assert session.timezone == zoneinfo.ZoneInfo("Europe/Madrid")
    assert session.app_version == 3
    assert session.device_info["manufacturer"] == "motorola"
    assert session.device_info["model"] == "moto g(30)"
    assert session.device_info["device"] == "caprip"
    assert session.device_info["android_version"] == "12"
    assert session.device_info["sdk_int"] == 31

    session_from_factory = SessionFactory.from_file(session_v4_file)
    assert session_from_factory.start_localized_instant == session.start_localized_instant
    assert session_from_factory.timezone == session.timezone
    assert session_from_factory.app_version == session.app_version
    assert session_from_factory.device_info == session.device_info
    assert session_from_factory.beacons.equals(session.beacons)
