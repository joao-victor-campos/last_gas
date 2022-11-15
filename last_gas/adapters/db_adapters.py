from last_gas.domain.ports import DBLoader
from sqlalchemy import create_engine, Column, String, Integer, CHAR, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Any, Dict, List
from datetime import datetime, timedelta
from last_gas.domain.schedulers.time_scheduler import get_now_time
import uuid

Base = declarative_base()


class PostgresLoader(DBLoader):
    def __init__(self, engine) -> None:
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get(self, orm_class, id: int, primary_key_name: int) -> Dict[str, Any]:
        return self.session.query(orm_class).filter(
            getattr(orm_class, primary_key_name) == id
        )

    def insert(
        self,
        orm_obj: object,
    ) -> None:
        self.session.add(orm_obj)
        self.session.commit()

    def update(
        self, orm_obj: object, primary_key_name: int, orm_class: int, params: Dict[str]
    ):
        self.session.query(orm_obj.__class__).filter(
            getattr(orm_obj, primary_key_name) == id
        ).update(params, synchronize_session="fetch")
