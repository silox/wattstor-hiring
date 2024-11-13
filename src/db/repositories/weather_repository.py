from datetime import datetime
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import WeatherData, WeatherRequest
from db.models.weather_model import WeatherModel


class WeatherRepository:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def get_weather(self, data: WeatherRequest):
        async with self.__db_session() as session:
            result = await session.execute(
                select(WeatherModel).where(
                    WeatherModel.name == data.name,
                    WeatherModel.latitude == data.latitude,
                    WeatherModel.longitude == data.longitude,
                )
            )
            weather_data = result.scalars().all()

        return weather_data

    async def create_weather(self, data: WeatherData):
        data.time = datetime.now()
        new_weather = WeatherModel(**data.model_dump())
        async with self.__db_session() as session:
            async with session.begin():
                session.add(new_weather)
            await session.commit()

    async def update_weather(self, data: WeatherData):
        async with self.__db_session() as session:
            async with session.begin():
                update_query = (
                    update(WeatherModel)
                    .where(
                        WeatherModel.name == data.name,
                        WeatherModel.latitude == data.latitude,
                        WeatherModel.longitude == data.longitude,
                    )
                    .values(
                        temperature=data.temperature,
                        wind_speed=data.wind_speed,
                        time=datetime.now(),
                    )
                )
                await session.execute(update_query)

            await session.commit()

    async def delete_weather(self, data: WeatherData):
        async with self.__db_session() as session:
            async with session.begin():
                delete_query = delete(WeatherModel).where(
                    WeatherModel.name == data.name,
                    WeatherModel.latitude == data.latitude,
                    WeatherModel.longitude == data.longitude,
                )
                await session.execute(delete_query)

            await session.commit()
