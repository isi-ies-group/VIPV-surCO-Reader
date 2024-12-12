import json

from .session_data_v1 import SessionDataV1


class SessionFactory:
    """
    Factory class to create a SessionData object from a file with the
    appropriate version scheme.
    """

    def _deduce_version_scheme(self):
        """
        Read the header of the file and get the json version scheme.
        The header is defined as the first lines of the file, until an empty
        line is found.
        """
        with open(self.file_path, "r") as file:
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
    def from_file(self, file_path):
        self.file_path = file_path
        version_scheme = self._deduce_version_scheme()
        match (version_scheme):
            case 1:
                return SessionDataV1.from_file(file_path)
            case _:
                raise ValueError("Invalid version scheme")
