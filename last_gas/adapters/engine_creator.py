from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class EngineCreator:
    """Create a Engine for database connection."""

    def __init__(
        self,
        database_flavour: str,
        user: str,
        password: str,
        host: str,
        database: str,
    ) -> None:
        """Initial Cronstructor.

        Args:
            database_flavour (str): Database flavour.
            user (str): Username.
            password (str): Password.
            host (str): Host.
            database (str): Database name.
        """
        self.database_flavour = database_flavour
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def create(self) -> Engine:
        """Engine creator.

        Returns:
            engine: Engine object from SQLAlchemy.
        """
        engine = create_engine(
            f"{self.database_flavour}+pg8000://{self.user}:{self.password}@{self.host}/{self.database}"
        )
        return engine
