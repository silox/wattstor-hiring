from dependency_injector import containers, providers
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from open_meteo import OpenMeteo
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.repositories.weather_repository import WeatherRepository
from services import InfluxService, MeteoService
import settings


class ApplicationContainer(containers.DeclarativeContainer):
    influx_service = providers.Singleton(
        InfluxService,
        client_class=InfluxDBClientAsync,
        url=settings.INFLUX_CLUSTER_URL,
        token=settings.INFLUX_TOKEN,
        organisation=settings.INFLUX_ORGANISATION,
        bucket_name=settings.INFLUX_BUCKET_NAME,
    )
    meteo_service = providers.Singleton(MeteoService, client_class=OpenMeteo)

    db_engine = providers.Singleton(create_async_engine, settings.POSTGRES_URL, echo=True)
    db_session = providers.Factory(sessionmaker, db_engine, expire_on_commit=False, class_=AsyncSession)
    weather_repository = providers.Singleton(WeatherRepository, db_session=db_session)
