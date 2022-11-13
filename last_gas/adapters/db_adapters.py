from last_gas.domain.ports import DBLoader
from sqlalchemy import create_engine, Column, String, Integer, CHAR, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Any, Dict, List
from datetime import datetime, timedelta
from last_gas.domain.schedulers.time_scheduler import get_now_time
import uuid

Base = declarative_base()


class Schedules(Base):
    tablename = "schedules"

    scedule_id = Column("scedule_id", Integer, primary_key=True)
    search_list = Column("search_list", ARRAY)
    times_of_day = Column("times_of_day", ARRAY)
    created_at = Column("create_at", DateTime)

    def __init__(self, scedule_id, search_list, created_at, times_of_day) -> None:
        self.scedule_id = scedule_id
        self.search_list = search_list
        self.times_of_day = times_of_day
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
        obj: List,
        scheduled_time: List,
    ) -> None:
        schedule = Schedules(uuid.uuid4(), obj, scheduled_time, get_now_time())
        self.session.add(schedule)
        self.session.commit()

    def update(self, obj: str, param, new_obj: str):
        self.session.query(Schedules).filter(Schedules.obj_name == obj).update()
