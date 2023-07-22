from dataclasses import dataclass
from typing import Literal


@dataclass
class ContentItem:
    media: str  # media source of the post or comment
    content_type: Literal["post", "comment"]  # post or comment
    author: str  # author of the post or comment
    post_id: str  # id of the post
    year: str  # year of the post
    board: str  # board of the post
    title: str  # title of the post
    text: str  # text of the post or comment
    rating: str  # rating of the comment
    order: int  # 0 for post, 1, 2, 3, ... for comments
    chunk: int  # if text too long, split into chunks
    total_chunks: int  # total number of chunks