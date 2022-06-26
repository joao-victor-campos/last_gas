from abc import ABC, abstractmethod
from typing import Any, Dict


class ConfigLoader(ABC):
    @abstractmethod
    def load_configs(self) -> Dict[str, Any]:
        pass
