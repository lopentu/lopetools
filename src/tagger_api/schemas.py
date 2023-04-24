from pydantic import BaseModel, Field


class TaggedToken(BaseModel):
    token: str = Field(..., description="The token")
    tag: str = Field(..., description="The POS tag")
    gloss: str = Field(..., description="The sense ID, gloss, and confidence level")


class TagInput(BaseModel):
    text: str = Field(..., description="The text to be tagged")


class TagOutput(BaseModel):
    tagged_text: list[list[TaggedToken]] = Field(..., description="The tagged text")
