from datetime import datetime, timedelta

from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from api.models import WeatherData, WeatherRequest


# Not working, getting error from influx while trying to delete data
class InfluxService:
    def __init__(self, client_class: InfluxDBClientAsync, url: str, token: str, organisation: str, bucket_name: str):
        self.__client_class = client_class
        self.__bucket_name = bucket_name
        self.__url = url
        self.__token = token
        self.__organisation = organisation
        self.__bucket_name = bucket_name

    async def test_get(self, data: WeatherRequest):
        async with self.__client_class(url=self.__url, token=self.__token, org=self.__organisation) as influx_client:

            query_api = influx_client.query_api()
            query = f"""from(bucket: "{self.__bucket_name}")
                |> range(start: -30d)
                |> filter(fn: (r) => r._measurement == "weather")
                """
            tables = await query_api.query(org=self.__organisation, query=query)
            print(tables)
            if tables:
                for table in tables:
                    for record in table.records:
                        print("Record:", record)  # Inspect each record

            output = tables.to_values(columns=["_measurement", "_field", "_time", "_value"])
            print(output)

    async def write_weather(self, data: WeatherData):
        async with self.__client_class(url=self.__url, token=self.__token) as influx_client:
            write_api = influx_client.write_api()
            point = Point.from_dict({"measurement": "weather", "fields": data.dict()}).time(datetime.now())
            await write_api.write(self.__bucket_name, self.__organisation, point)

    async def delete_weather(self, data: WeatherRequest):
        async with self.__client_class(url=self.__url, token=self.__token) as influx_client:
            query_api = influx_client.delete_api()
            await query_api.delete(
                datetime.now() - timedelta(days=30),
                datetime.now(),
                '_measurement="weather"',
                org=self.__organisation,
                bucket=self.__bucket_name,
            )
