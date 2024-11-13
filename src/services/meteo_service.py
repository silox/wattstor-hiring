from typing import Type

from open_meteo import OpenMeteo

from api.models import WeatherData, WeatherRequest


class MeteoService:
    def __init__(self, client_class: Type[OpenMeteo]):
        self.__client_class = client_class

    async def get_weather(self, data: WeatherRequest) -> WeatherData:
        async with self.__client_class() as meteo_client:
            meteo_result = await meteo_client.forecast(
                latitude=data.latitude,
                longitude=data.longitude,
                current_weather=True,
            )

            return WeatherData(
                name=data.name,
                latitude=meteo_result.latitude,
                longitude=meteo_result.longitude,
                temperature=meteo_result.current_weather.temperature,
                wind_speed=meteo_result.current_weather.wind_speed,
                time=meteo_result.current_weather.time,
            )
