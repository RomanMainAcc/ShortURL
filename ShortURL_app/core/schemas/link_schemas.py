from pydantic import BaseModel, HttpUrl


class Link(BaseModel):
    link: HttpUrl
