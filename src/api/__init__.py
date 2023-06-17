from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .v1.routers import agent, tagger


def create_app() -> FastAPI:

    origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8005",
    ]

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(agent.agent_router)
    app.include_router(tagger.tagger_router)

    return app
