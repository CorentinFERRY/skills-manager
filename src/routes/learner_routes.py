from typing import List

from fastapi import APIRouter, Header, HTTPException

from src.schemas.learner_schema import LearnerCreate, LearnerResponse
from src.services import learner_service

router = APIRouter()


@router.get("/apprenants")
def get_all() -> List[LearnerResponse]:
    learners = learner_service.get_all_learners()
    return [LearnerResponse(id=learner.id, name=learner.name) for learner in learners]


@router.post("/apprenants", status_code=201)
def create(body: LearnerCreate, x_role: str = Header(...)) -> LearnerResponse:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    learner = learner_service.create_learner(body.name)
    return LearnerResponse(id=learner.id, name=learner.name)


@router.get("/apprenants/{id}")
def get_by_id(id: int) -> LearnerResponse:
    learner = learner_service.get_learner_by_id(id)
    if not learner:
        raise HTTPException(status_code=404, detail="Apprenant non trouvé !")
    return LearnerResponse(id=learner.id, name=learner.name)


@router.put("/apprenants/{id}")
def update(id: int, body: LearnerCreate) -> LearnerResponse:
    updated_learner = learner_service.update_learner(id, body)
    if not updated_learner:
        raise HTTPException(status_code=404, detail="Apprenant non trouvé !")
    return LearnerResponse(id=updated_learner.id, name=updated_learner.name)


@router.delete("/apprenants/{id}", status_code=204)
def delete(id: int, x_role: str = Header(...)) -> None:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    deleted = learner_service.delete_learner(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Apprenant non trouvé !")
