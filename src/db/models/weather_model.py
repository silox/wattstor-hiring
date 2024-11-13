import uuid

from sqlalchemy import Column, Float, DateTime, String, orm, UUID

Base = orm.declarative_base()


class WeatherModel(Base):
    __tablename__ = 'weather'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    time = Column(DateTime, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    wind_speed = Column(Float)
