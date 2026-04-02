from typing import List

from fastapi import APIRouter, Header, HTTPException

from src.schemas.trainer_schema import TrainerCreate, TrainerResponse
from src.services import trainer_service

router = APIRouter()


@router.get("/formateurs")
def get_all() -> List[TrainerResponse]:
    trainers = trainer_service.get_all_trainers()
    return [TrainerResponse(id=trainer.id, name=trainer.name) for trainer in trainers]


@router.get("/formateurs/{id}")
def get_by_id(id: int) -> TrainerResponse:
    trainer = trainer_service.get_trainer_by_id(id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Formateur non trouvé !")
    return TrainerResponse(id=trainer.id, name=trainer.name)


@router.post("/formateurs", status_code=201)
def create(body: TrainerCreate, x_role: str = Header(...)) -> TrainerResponse:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    trainer = trainer_service.create_trainer(body.name)
    return TrainerResponse(id=trainer.id, name=trainer.name)


@router.put("/formateurs/{id}")
def update(id: int, body: TrainerCreate, x_role: str = Header(...)) -> TrainerResponse:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    updated_trainer = trainer_service.update_trainer(id, body)
    if not updated_trainer:
        raise HTTPException(status_code=404, detail="Formateur non trouvé !")
    return TrainerResponse(id=updated_trainer.id, name=updated_trainer.name)


@router.delete("/formateurs/{id}", status_code=204)
def delete(id: int, x_role: str = Header(...)):
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    deleted = trainer_service.delete_trainer(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Formateur non trouvé !")
