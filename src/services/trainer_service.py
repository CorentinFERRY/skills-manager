from typing import List

from src.models.Trainer import Trainer
from src.repositories import trainer_repository
from src.schemas.trainer_schema import TrainerCreate


def get_all_trainers() -> List[Trainer]:
    trainers = trainer_repository.find_all()
    return [Trainer(id=trainer["id"], name=trainer["name"]) for trainer in trainers]


def get_trainer_by_id(trainer_id: int) -> Trainer | None:
    trainer = trainer_repository.find_by_id(trainer_id)
    if not trainer:
        return None
    return Trainer(id=trainer["id"], name=trainer["name"])


def create_trainer(name: str) -> Trainer:
    trainer_id = trainer_repository.insert(name)
    return Trainer(id=trainer_id, name=name)


def update_trainer(trainer_id: int, data: TrainerCreate) -> Trainer | None:
    update = trainer_repository.update(trainer_id, data.name)
    if not update:
        return None
    return Trainer(id=trainer_id, name=data.name)


def delete_trainer(trainer_id: int) -> bool:
    return trainer_repository.delete(trainer_id)
