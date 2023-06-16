from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE / "dwsd-beta"))

from fastapi import APIRouter, Query  # noqa: E402
from DistilTag import DistilTag  # noqa: E402

from ...tagger.schemas import TagOutput, TaggedToken  # noqa: E402
from dotted_wsd import DottedWsdTagger  # noqa: E402

distil_tagger = DistilTag()
dwsd = DottedWsdTagger()

tagger_router = APIRouter(prefix="/tagger", tags=["tagger"])


@tagger_router.get("/", response_model=TagOutput, status_code=200)
def tag(
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
