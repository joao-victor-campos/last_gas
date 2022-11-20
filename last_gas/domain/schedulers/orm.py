from sqlalchemy import Column, String, Integer, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SchedulesTypes(Base):
    __tablename__ = "schedules_types"

    schedule_type_id = Column("schedule_type_id", Integer, primary_key=True)
    schedule_type = Column("schedule_type", String)

    def __init__(self, schedule_type_id, schedule_type) -> None:
        self.schedule_type_id = schedule_type_id
        self.schedule_type = schedule_type


class Schedules(Base):
    __tablename__ = "schedules"

    schedule_id = Column("schedule_id", Integer, primary_key=True)
    days_of_week = Column("days_of_week", ARRAY(String))
    times_of_day = Column("times_of_day", ARRAY(String))
    args = Column("args", ARRAY(String), nullable=True)
    kwargs = Column("kwargs", String, nullable=True)
    created_at = Column("created_at", DateTime)
    updated_at = Column("updated_at", DateTime)
    schedule_type_id = Column(
        "schedule_type_id", Integer, ForeignKey("schedules_types.schedule_type_id")
    )
    child = relationship("SchedulesTypes")

    def __init__(
        self,
        scedule_id,
        search_list,
        args,
        kwargs,
        created_at,
        updated_at,
        times_of_day,
        days_of_week,
        schedule_type_id,
    ) -> None:
        self.scedule_id = scedule_id
        self.search_list = search_list
        self.args = args
        self.kwargs = kwargs
        self.days_of_week = days_of_week
        self.times_of_day = times_of_day
        self.created_at = created_at
        self.updated_at = updated_at
        self.schedule_type_id = schedule_type_id
