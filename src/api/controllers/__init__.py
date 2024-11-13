from api.controllers.weather_controller import weather_router, WeatherController
from api.controllers.index_controller import index_router, IndexController


router_list = [
    index_router,
    weather_router,
]

__all__ = [
    "weather_router",
    "WeatherController",
    "index_router",
    "IndexController",
]
