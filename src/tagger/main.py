from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.resolve() / "dwsd-beta"))

from fastapi import FastAPI, APIRouter, Query  # noqa: E402
from DistilTag import DistilTag  # noqa: E402

from schemas import TagOutput, TaggedToken  # noqa: E402
from dotted_wsd import DottedWsdTagger  # noqa: E402

distil_tagger = DistilTag()
dwsd = DottedWsdTagger()

app = FastAPI(
    title="LOPE API", description="API for LOPE tools", openapi_url="/openapi.json"
)

api_router = APIRouter()


@api_router.get("/tag/", response_model=TagOutput, status_code=200)
def tag(
    text: str = Query(
        ..., description="The text to be tagged", example="星巴克宣布明天起停賣星巴克"
    )
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

# cwn_api_router = APIRouter(prefix="/cwn", tags=["cwn"])
# @cwn_api_router.get("/", status_code=200)


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")
