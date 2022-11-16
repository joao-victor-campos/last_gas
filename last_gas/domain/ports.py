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
    def get(self, id: int, obj: str, url: str) -> Dict[str, Any]:
        """Get data from a postgres database.

        Args:
            query (str): Query string
            url (str): postgres url to retrieve data.

        Returns:
            Dict[str, Any]: data.
        """
        pass

    @abstractmethod
    def insert(self, orm_obj: object) -> None:
        """Insert a regestry to a databse.

        Args:
            obj (str): List[str]
            scheduled_time (str): List[str]
        """
        pass

    def update(
        self, orm_obj: object, primary_key_name: int, params: Dict[str, Any]
    ) -> None:
        pass
