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
    def get(self, orm_class, id: int) -> Dict[str, Any]:
        """Get data from a postgres database.

        Args:
            orm_class (class): ORM table class.
            id (str): Primary key.

        Returns:
            Dict[str, Any]: data.
        """
        pass

    @abstractmethod
    def insert(self, orm_obj: object) -> None:
        """Insert a regestry to a databse.

        Args:
            orm_obj (object): ORM table class.
        """
        pass

    @abstractmethod
    def update(
        self,
        table_class: object,
        primary_key_name: str,
        new_values: Dict[str, Any],
        id: int,
    ) -> None:
        """Update a regestry on the database.

        Args:
            table_class (object): ORM table class.
            primary_key_name (str): Column name.
            new_values (Dict[str, Any]): New values to be updated.
            id (int): Primary key.
        """
        pass

    def delete(
        self,
        table_class: object,
        primary_key_name: str,
        id: int,
    ) -> None:
        """Delete a regestry on the database.

        Args:
            table_class (object): ORM table class.
            primary_key_name (str): Column name.
            id (int): Primary key.
        """
        pass
