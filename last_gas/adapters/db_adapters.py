from last_gas.domain.ports import DBLoader
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Any, Dict

Base = declarative_base()


class PostgresLoader(DBLoader):
    def __init__(self, engine) -> None:
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get(self, orm_class, id: int) -> Dict[str, Any]:
        return {
            key: val
            for key, val in self.session.query(orm_class).get(id).__dict__.items()
            if not key.startswith("_")
        }

    def get_all(self, orm_class, id: int) -> Dict[str, Any]:
        return {
            key: val
            for key, val in self.session.query(orm_class).all().__dict__.items()
            if not key.startswith("_")
        }

    def insert(self, orm_obj: object) -> None:
        self.session.add(orm_obj)
        self.session.commit()

    def update(
        self,
        table_class: object,
        primary_key_name: str,
        new_values: Dict[str, Any],
        id: int,
    ) -> None:
        self.session.query(table_class).filter(
            getattr(table_class, primary_key_name) == id
        ).update(new_values, synchronize_session="fetch")
        self.session.commit()

    def delete(
        self,
        table_class: object,
        primary_key_name: str,
        id: int,
    ) -> None:
        self.session.query(table_class).filter(
            getattr(table_class, primary_key_name) == id
        ).delete()
        self.session.commit()
