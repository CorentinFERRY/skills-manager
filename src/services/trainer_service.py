from typing import List

import src.database.memory as memory
from src.models.Trainer import Trainer
from src.schemas.trainer_schema import TrainerCreate


def get_all_trainers() -> List[Trainer]:
    return memory.trainers


def get_trainer_by_id(trainer_id: int) -> Trainer | None:
    for trainer in memory.trainers:
        if trainer.id == trainer_id:
            return trainer
    return None


def create_trainer(name: str) -> Trainer:
    new_trainer = Trainer(id=memory.current_trainer_id, name=name)
    memory.current_trainer_id += 1
    memory.trainers.append(new_trainer)
    return new_trainer


def update_trainer(trainer_id: int, data: TrainerCreate) -> Trainer | None:
    for i, trainer in enumerate(memory.trainers):
        if trainer.id == trainer_id:
            trainer.name = data.name
            return trainer
    return None


def delete_trainer(trainer_id: int) -> Trainer | None:
    for i, trainer in enumerate(memory.trainers):
        if trainer.id == trainer_id:
            return memory.trainers.pop(i)
    return None
