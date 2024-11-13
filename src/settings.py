import dotenv
import os

dotenv.load_dotenv()

INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_CLUSTER_URL = os.getenv("INFLUX_CLUSTER_URL")
INFLUX_ORGANISATION = os.getenv("INFLUX_ORGANISATION")
INFLUX_BUCKET_NAME = os.getenv("INFLUX_BUCKET_NAME")

POSTGRES_URL = os.getenv("POSTGRES_URL")
