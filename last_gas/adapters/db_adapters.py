from last_gas.domain.ports import DBLoader
from sqlalchemy import create_engine, Column, String, Integer, CHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Any, Dict
from datetime import datetime
import uuid

Base = declarative_base()


class Schedules(Base):
    tablename = "schedules"

    schedule_id = Column("schedule_id", Integer, primary_key=True)
    obj_name = Column("obj_name", String)
    datetime_scheduled = Column("datetime_scheduled", DateTime)
    created_at = Column("create_at", DateTime)

    def __init__(self, schedule_id, obj_name, datetime_scheduled, created_at) -> None:
        self.schedule_id = schedule_id
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
        schedule = Schedules(
            uuid.uuid4(),
            obj,
            scheduled_time,
            datetime.now()
        )
        self.session.add(schedule)
        self.session.commit()

    def update():
        pass
