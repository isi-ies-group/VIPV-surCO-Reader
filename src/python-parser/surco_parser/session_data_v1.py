import pandas as pd

import json
from base64 import b64decode


class SessionDataV1:
    version_scheme = 1
    start_instant: pd.Timestamp
    finish_instant: pd.Timestamp
    beacons: pd.DataFrame
    measurements: pd.DataFrame

    def __init__(self, start_instant, finish_instant, beacons, measurements):
        self.start_instant = start_instant
        self.finish_instant = finish_instant
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
            pd.Timestamp(header["start_instant"]),
            pd.Timestamp(header["finish_instant"]),
            beacons,
            measurements,
        )
