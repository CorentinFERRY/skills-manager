from typing import List

from src.repositories import learner_repository
from src.models.Learner import Learner
from src.schemas.learner_schema import LearnerCreate


def get_all_learners() -> List[Learner]:
    learners = learner_repository.find_all()
    return [Learner(id = learner["id"], name = learner["name"]) for learner in learners]


def get_learner_by_id(learner_id: int) -> Learner | None:
    learner = learner_repository.find_by_id(learner_id)
    if not learner:
        return None
    learner = Learner(id = learner["id"], name = learner["name"])
    for skill in learner_repository.find_validated_skills(learner_id):
        learner.add_validated_skill(skill["skill_id"])
    return learner


def create_learner(name: str) -> Learner:
    learner_id = learner_repository.insert(name)
    return Learner(id=learner_id, name=name)


def update_learner(learner_id: int, data: LearnerCreate) -> Learner | None:
    updated = learner_repository.update(learner_id, data.name)
    if not updated:
        return None
    return Learner(id=learner_id, name=data.name)


def delete_learner(learner_id: int) -> bool:
    return learner_repository.delete(learner_id)
