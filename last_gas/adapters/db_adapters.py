from last_gas.domain.ports import DBLoader
from sqlalchemy import create_engine, Column, String, Integer, CHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Any, Dict
from datetime import datetime, timedelta
from last_gas.domain.schedulers.time_scheduler import get_now_time
import uuid

Base = declarative_base()


class Schedules(Base):
    tablename = "schedules"

    obj_name = Column("obj_name", String, primary_key=True)
    datetime_scheduled = Column("datetime_scheduled", DateTime)
    created_at = Column("create_at", DateTime)

    def __init__(self, obj_name, datetime_scheduled, created_at) -> None:
        self.obj_name = obj_name
        self.datetime_scheduled = datetime_scheduled
        self.created_at = created_at


class PostgresLoader(DBLoader):
    def __init__(self, engine) -> None:
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get(self, obj: str) -> Dict[str, Any]:
        return self.session.query(Schedules).filter(Schedules.obj_name == obj)

    def insert(
        self,
        obj: str,
        scheduled_time: str,
    ) -> None:
        schedule = Schedules(uuid.uuid4(), obj, scheduled_time, get_now_time())
        self.session.add(schedule)
        self.session.commit()

    def update(self, obj: str, param, new_obj: str):
        self.session.query(Schedules).filter(Schedules.obj_name == obj).update()
