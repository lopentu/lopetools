from fastapi import FastAPI
from src.api.v1.types import APIRequest, APIResponse
from src.lc_tools.agents import LOPEAgent

def create_app() -> FastAPI:

    app = FastAPI()

    @app.post("/")
    async def call_model(request: APIRequest) -> APIResponse:
        text = request.text
        messages = request.messages
        tools = request.tools
        openai_api_key = request.openai_api_key
        agent = LOPEAgent(
            messages=messages,
            tools=tools,
            openai_api_key=openai_api_key,
        )
        response = agent(text)
        return APIResponse(**response)

