from pydantic import BaseModel


class APIResponse(BaseModel):
    formatted: list 
    raw: list


class APIRequest(BaseModel):
    text: str
    messages: list  # used for loading previous messages
    use_cwn: bool
    use_asbc: bool
    use_ptt: bool
    openai_api_key: str | None = None