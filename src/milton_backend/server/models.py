from pydantic import BaseModel


class QueryModel(BaseModel):
    user_query: str
