from pydantic import BaseModel


class TrainerCreate(BaseModel):
    name: str


class TrainerResponse(BaseModel):
    id: int
    name: str
