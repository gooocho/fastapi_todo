from fastapi.applications import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()
    return app
