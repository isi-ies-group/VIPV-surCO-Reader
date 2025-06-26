import pandas as pd
import json
from base64 import b64decode
from zoneinfo import ZoneInfo
from typing import TypedDict


class DeviceInfoV5(TypedDict):
    manufacturer: str
    model: str
    device: str
    android_version: str
    sdk_int: int


class SessionDataV5:
    version_scheme = 5
    app_version: int
    timezone: ZoneInfo
    start_localized_instant: pd.Timestamp
    finish_localized_instant: pd.Timestamp
    beacons: pd.DataFrame
    measurements: pd.DataFrame

    device_info: DeviceInfoV5

    def __init__(
        self,
        app_version,
        timezone,
        start_localized_instant,
        finish_localized_instant,
        device_info,
        beacons,
        measurements,
    ):
        self.app_version = int(app_version)
        if isinstance(timezone, str):
            self.timezone = ZoneInfo(timezone)
        else:
            self.timezone = timezone
        self.start_localized_instant = start_localized_instant
        self.finish_localized_instant = finish_localized_instant
        self.device_info = device_info
        self.beacons = beacons
        self.measurements = measurements

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r") as file:
            # read the header lines
            header = []
            for line in file:
                if line == "\n":
                    break
                header.append(line)
            # read the rest of the file as a csv
            measurements = pd.read_csv(file_path, skiprows=1)
        header = "".join(header)
        header = json.loads(header)

        if header["version_scheme"] != cls.version_scheme:
            raise ValueError("Invalid version scheme")

        beacons = pd.DataFrame(header["beacons"])
        beacons = beacons.set_index("id")
        # decode descriptions from base64 in utf-8
        beacons["description"] = beacons["description"].map(
            lambda incoded: b64decode(incoded).decode("utf-8")
        )

        return cls(
            header["app_version"],
            header["timezone"],
            pd.Timestamp(header["start_localized_instant"]),
            pd.Timestamp(header["finish_localized_instant"]),
            header["device_info"],
            beacons,
            measurements,
        )
