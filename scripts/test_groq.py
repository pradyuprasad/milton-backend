import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor
from . import Config
config = Config()

client = Groq(
    api_key=config.get('GROQ_API_KEY'),
)

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

resp = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the company Tesla",
        }
    ],
    response_model=Character,
)
print(resp.model_dump_json(indent=2))
