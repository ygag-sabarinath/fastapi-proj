from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str #| None = None
    published : bool  | None = None