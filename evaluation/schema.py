from pydantic import BaseModel


class JudgeScore(BaseModel):
    faithfulness: int
    relevance: int
    reasoning: str


JSON_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    "required": ["name", "age"],
}
