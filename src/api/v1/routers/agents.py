from pathlib import Path
import os
import sys

# sys.path.append(str(BASE / "src"))
from dotenv import load_dotenv
from fastapi import APIRouter
from loguru import logger

from api.types import APIRequest, APIResponse
from lc_tools.agents import LOPEAgent

BASE = Path(__file__).resolve().parent.parent.parent.parent.parent
load_dotenv(BASE / ".env")


# def create_app() -> FastAPI:

agent_router = APIRouter(prefix="/agent", tags=["agent"])



# async def call_model(request: APIRequest) -> APIResponse:
@agent_router.post("/")
async def call_model(request: APIRequest) -> APIResponse:
    logger.info(request.dict())
    # return request.dict()
    text = request.text
    messages = request.messages
    use_asbc = request.use_asbc
    use_cwn = request.use_cwn
    openai_api_key = request.openai_api_key
    if not openai_api_key:
        openai_api_key = os.environ["OPENAI_API_KEY"]
    agent = LOPEAgent(
        messages=messages,
        use_asbc=use_asbc,
        use_cwn=use_cwn,
        openai_api_key=openai_api_key,
    )
    response = agent(text)
    return APIResponse(**response)
