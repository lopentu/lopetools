from pathlib import Path
import sys


from fastapi import FastAPI, APIRouter, Query  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from loguru import logger
from DistilTag import DistilTag  # noqa: E402
from pydantic import BaseModel  # noqa: E402

BASE = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE / "dwsd-beta"))
from dotted_wsd import DottedWsdTagger  # noqa: E402
from .schemas import TagOutput, TaggedToken  # noqa: E402

distil_tagger = DistilTag()
dwsd = DottedWsdTagger()
logger.info("Tagger loaded.")

tagger_router = APIRouter()


class TagRequest(BaseModel):
    text: str


@tagger_router.get("/tag/", response_model=TagOutput, status_code=200)
async def tag(
    text: str = Query(..., description="The text to be tagged", example="星巴克宣布明天起停賣星巴克")
):
    tagged_text = distil_tagger.tag(text)
    tagged_text = [dwsd.sense_tag_per_sentence(sent) for sent in tagged_text]
    res = []
    for sent in tagged_text:
        res.append(
            [
                TaggedToken(token=token, tag=tag, gloss=gloss)
                for token, tag, gloss in sent
            ]
        )
    return TagOutput(tagged_text=res)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(tagger_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
