from abc import ABC, abstractmethod
from typing import Any, Dict


class ConfigLoader(ABC):
    @abstractmethod
    def load_configs(self) -> Dict[str, Any]:
        """Returns a dictonary from a environment variable

        :return: Dictonary with the security token
        :rtype: Dict[str, Any]
        """
        pass


class APILoader(ABC):
    @abstractmethod
    def query(self, query: str, url: str) -> Dict[str, Any]:
        """Queries an API endpoint.

        :param query: Query string.
        :type query: str
        :param url: url to retrieve data.
        :type url: str
        :return: Returns a dictonary from an API query respons
        :rtype: Dict[str, Any]
        """
        pass


class DBLoader(ABC):
    @abstractmethod
    def query_db(self, query: str, url: str) -> Dict[str, Any]:
        """Queries a postgres database.

        Args:
            query (str): Query string
            url (str): postgres url to retrieve data.

        Returns:
            Dict[str, Any]: data.
        """
        pass
