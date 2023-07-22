from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .v1.routers import agents


def create_app() -> FastAPI:

    # can't add tagger to the same app because it hangs
    app = FastAPI()

    app.include_router(agents.agent_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
