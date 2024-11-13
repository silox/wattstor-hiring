from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi_utils.cbv import cbv

from dependency_injector.wiring import Provide, inject

from api.models import WeatherRequest, WeatherData
from containers import ApplicationContainer
from services import MeteoService, InfluxService


weather_router = APIRouter(tags=["Weather"])


@cbv(weather_router)
class WeatherController:
    @inject
    def __init__(
        self,
        meteo_service: MeteoService = Depends(Provide[ApplicationContainer.meteo_service]),
        weather_repository: InfluxService = Depends(Provide[ApplicationContainer.weather_repository]),
    ):
        self.__meteo_service = meteo_service
        self.__weather_repository = weather_repository

    @weather_router.get("/weather")
    async def get_weather(self, data: Annotated[WeatherRequest, Query()]):
        response_data = await self.__weather_repository.get_weather(data)
        return response_data

    @weather_router.post("/weather", status_code=status.HTTP_201_CREATED)
    async def create_weather(self, data: WeatherData):
        await self.__weather_repository.create_weather(data)
        return data

    @weather_router.put("/weather")
    async def update_weather(self, data: WeatherData):
        await self.__weather_repository.update_weather(data)
        return data

    @weather_router.delete("/weather", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_weather(self, data: WeatherRequest):
        await self.__weather_repository.delete_weather(data)
        return None

    @weather_router.post("/fetch-weather")
    async def fetch_forecast(self, data: WeatherRequest):
        meteo_response = await self.__meteo_service.get_weather(data)
        await self.__weather_repository.create_weather(meteo_response)

        return meteo_response
