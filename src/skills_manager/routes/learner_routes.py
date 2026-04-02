from typing import List

from fastapi import APIRouter, Header, HTTPException

from skills_manager.models.Learner import Learner
from skills_manager.schemas.learner_schema import LearnerCreate
from skills_manager.services import learner_service

router = APIRouter()


@router.get("/apprenants")
def get_learners() -> List[Learner]:
    return learner_service.get_all_learners()


@router.post("/apprenants", status_code=201)
def create_learner(body: LearnerCreate, x_role: str = Header(...)) -> Learner:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    return learner_service.create_learner(body.name)


@router.get("/apprenants/{id}")
def get_learner_by_id(id: int) -> Learner:
    learner = learner_service.get_learner_by_id(id)
    if not learner:
        raise HTTPException(status_code=404, detail="Apprenant non trouvé !")
    return learner


@router.put("/apprenants/{id}")
def update_learner(id: int, body: LearnerCreate) -> Learner:
    updated_learner = learner_service.update_learner(id, body)
    if not updated_learner:
        raise HTTPException(status_code=404, detail="Apprenant non trouvé !")
    return updated_learner


@router.delete("/apprenants/{id}", status_code=204)
def delete_learner(id: int, x_role: str = Header(...)) -> None:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    deleted = learner_service.delete_learner(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Apprenant non trouvé !")
