from pydantic import BaseConfig, BaseModel, Field


class Text(BaseModel):
    text: str