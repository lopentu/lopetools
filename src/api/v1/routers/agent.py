from pathlib import Path
import sys

# BASE = Path(__file__).resolve().parent.parent.parent
# sys.path.append(str(BASE / "src"))
from fastapi import APIRouter
from loguru import logger

from api.types import APIRequest, APIResponse
from lc_tools.agents import LOPEAgent


# def create_app() -> FastAPI:

agent_router = APIRouter(prefix="/agent", tags=["agent"])



# async def call_model(request: APIRequest) -> APIResponse:
@agent_router.post("/")
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
