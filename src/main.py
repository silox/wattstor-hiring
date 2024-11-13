from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.controllers import router_list
from containers import ApplicationContainer


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = ApplicationContainer()
    container.wire(modules=["api.controllers.weather_controller"])
    yield


def create_app():
    app = FastAPI(redoc_url=None, lifespan=lifespan)
    for app_router in router_list:
        app.include_router(app_router)

    return app


app = create_app()
