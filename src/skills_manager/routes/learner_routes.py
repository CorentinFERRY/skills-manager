from fastapi import APIRouter, Header, HTTPException

from skills_manager.schemas.learner_schema import LearnerCreate
from skills_manager.services import learner_service

router = APIRouter()


@router.get("/apprenants")
def get_learners():
    return learner_service.get_all_learners()


@router.post("/apprenants", status_code=201)
def create_learner(body: LearnerCreate, x_role: str = Header(...)):
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    return learner_service.create_learner(body.name)
