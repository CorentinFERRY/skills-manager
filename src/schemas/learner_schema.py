from pydantic import BaseModel


class LearnerCreate(BaseModel):
    name: str


class LearnerResponse(BaseModel):
    id: int
    name: str
