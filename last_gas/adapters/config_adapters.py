from typing import Any, Dict
import os
import yaml
import json


from last_gas.domain.ports import ConfigLoader
from last_gas.domain.exceptions import InvalidFileExtensionError


class LocalFileConfigLoader(ConfigLoader):
    def __init__(self, file_location: str) -> None:
        self._file_location = file_location

    def load_configs(self) -> Dict[str, Any]:
        file_extension = self._file_location.split(".")[-1]
        if file_extension == "yaml":
            with open(self._file_location, "r") as config_file:
                return yaml.safe_load(config_file)
        elif file_extension == "json":
            with open(self._file_location, "r") as config_file:
                return json.load(config_file)
        raise InvalidFileExtensionError(
            "Tried to load file '%s'  with unsuported extension '%s'"
            % (self._file_location, file_extension)
        )


class EnvVarConfigLoader(ConfigLoader):
    def load_configs(self) -> Dict[str, Any]:
        return os.environ
