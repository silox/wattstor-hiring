import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from api.controllers import WeatherController, weather_router
from api.models import WeatherRequest, WeatherData

client = TestClient(weather_router)

mock_weather_request = WeatherRequest(name="Prague", latitude=50.0755, longitude=14.4378)
mock_weather_data = WeatherData(
    name="Prague", latitude=50.0755, longitude=14.4378, temperature=22.5, wind_speed=5.0, time="2021-08-01T12:00:00"
)


mocked_repo_response = "mocked_repo_response"
mocked_meteo_response = "mocked_meteo_response"


@pytest.fixture
def mock_meteo_service():
    service = AsyncMock()
    service.get_weather = AsyncMock(return_value=mocked_meteo_response)
    return service


@pytest.fixture
def mock_weather_repository():
    repository = AsyncMock()
    repository.get_weather = AsyncMock(return_value=mocked_repo_response)
    repository.create_weather = AsyncMock(return_value=mocked_repo_response)
    repository.update_weather = AsyncMock(return_value=mocked_repo_response)
    repository.delete_weather = AsyncMock(return_value=mocked_repo_response)
    return repository


@pytest.fixture
def weather_controller(mock_meteo_service, mock_weather_repository):
    return WeatherController(meteo_service=mock_meteo_service, weather_repository=mock_weather_repository)


@pytest.mark.asyncio
async def test_get_weather(weather_controller):
    response = await weather_controller.get_weather(mock_weather_request)

    weather_controller._WeatherController__weather_repository.get_weather.assert_called_once_with(mock_weather_request)
    assert response == mocked_repo_response


@pytest.mark.asyncio
async def test_create_weather(weather_controller):

    response = await weather_controller.create_weather(mock_weather_data)

    weather_controller._WeatherController__weather_repository.create_weather.assert_called_once_with(mock_weather_data)
    assert response == mock_weather_data


@pytest.mark.asyncio
async def test_update_weather(weather_controller):
    response = await weather_controller.update_weather(mock_weather_data)

    weather_controller._WeatherController__weather_repository.update_weather.assert_called_once_with(mock_weather_data)
    assert response == mock_weather_data


@pytest.mark.asyncio
async def test_delete_weather(weather_controller):
    response = await weather_controller.delete_weather(mock_weather_data)

    weather_controller._WeatherController__weather_repository.delete_weather.assert_called_once_with(mock_weather_data)
    assert response is None


@pytest.mark.asyncio
async def test_fetch_forecast(weather_controller):
    response = await weather_controller.fetch_forecast(mock_weather_data)

    weather_controller._WeatherController__meteo_service.get_weather.assert_called_once_with(mock_weather_data)
    weather_controller._WeatherController__weather_repository.create_weather.assert_called_once()
    assert response == mocked_meteo_response
