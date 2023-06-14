from pathlib import Path
import sys

# BASE = Path(__file__).resolve().parent.parent.resolve()
# sys.path.append(str(BASE / "src"))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api.types import APIRequest, APIResponse
from src.lc_tools.agents import LOPEAgent


def create_app() -> FastAPI:

    app = FastAPI()

    origins = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # async def call_model(request: APIRequest) -> APIResponse:
    @app.post("/")
    async def call_model(request: APIRequest) -> dict:
        logger.info(request.dict())
        return request.dict()
        # text = request.text
        # messages = request.messages
        # tools = request.tools
        # openai_api_key = request.openai_api_key
        # agent = LOPEAgent(
        #     messages=messages,
        #     tools=tools,
        #     openai_api_key=openai_api_key,
        # )
        # response = agent(text)
        # return APIResponse(**response)

    return app