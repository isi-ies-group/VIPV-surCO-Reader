from measurements_parser import SessionDataV1

import pandas as pd
import pytest

from conftest import TEST_DATA_DIR


@pytest.fixture
def session_data_v1(tmpdir):
    """
    Create a temp file with the content of a session data v1 file.
    """
    header_file = TEST_DATA_DIR / "v1_header.txt"
    measurements_file = TEST_DATA_DIR / "v1_body.txt"
    temp_file = tmpdir / "session_data_v1.txt"
    with (
        open(temp_file, "w") as session_data_v1,
        open(header_file, "r") as header,
        open(measurements_file, "r") as body,
    ):
        # write content of both files to the temp file, but remove all newlines
        # and whitespaces from header first
        session_data_v1.write(header.read().replace("\n", "").replace(" ", ""))
        session_data_v1.write("\n\n")  # separator between header & body
        session_data_v1.write(body.read())
    return temp_file


def test_SessionDataV1_from_file(session_data_v1):
    session_data = SessionDataV1.from_file(session_data_v1)
    assert session_data.start_instant == pd.Timestamp("2021-10-01T12:00:00Z")
    assert session_data.finish_instant == pd.Timestamp("2021-10-01T12:30:00Z")
    assert session_data.beacons.columns.tolist() == [
        "tilt",
        "orientation",
        "description",
    ]
    assert session_data.beacons.index.tolist() == [
        "0x010203040506",
        "0x010203040507",
    ]
    assert (
        session_data.beacons.iloc[0]["description"]
        == "Soy la cosita más linda y mona de este mundo."
    )
