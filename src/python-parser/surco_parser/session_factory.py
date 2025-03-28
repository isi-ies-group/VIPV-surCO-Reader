import json

from .session_data_v1 import SessionDataV1
from .session_data_v3 import SessionDataV3
from .session_data_v4 import SessionDataV4


class SessionFactory:
    """
    Factory class to create a SessionData object from a file with the
    appropriate version scheme.
    """

    @classmethod
    def _deduce_version_scheme(cls, file_path):
        """
        Read the header of the file and get the json version scheme.
        The header is defined as the first lines of the file, until an empty
        line is found.
        """
        with open(file_path, "r") as file:
            header = []
            for line in file:
                if line == "\n":
                    break
                header.append(line)
            else:
                raise ValueError("Invalid file format")
        header = "".join(header)
        header = json.loads(header)
        return header["version_scheme"]

    @classmethod
    def from_file(cls, file_path):
        version_scheme = cls._deduce_version_scheme(file_path)
        match (version_scheme):
            case 1:
                return SessionDataV1.from_file(file_path)
            case 3:
                return SessionDataV3.from_file(file_path)
            case 4:
                return SessionDataV4.from_file(file_path)
            case _:
                raise ValueError(f"Invalid version scheme {version_scheme}")
