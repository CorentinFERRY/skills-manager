from typing import List

import skills_manager.database.memory as memory
from skills_manager.models.Learner import Learner


def get_all_learners() -> List[Learner]:
    return memory.learners


def get_learner_by_id(learner_id: int) -> Learner | None:
    for learner in memory.learners:
        if learner.id == learner_id:
            return learner
    return None


def create_learner(name: str) -> Learner:
    new_learner = Learner(id=memory.current_learner_id, name=name)
    memory.current_learner_id += 1
    memory.learners.append(new_learner)
    return new_learner


def update_learner(learner_id: int, updated_learner: Learner) -> Learner | None:
    for i, learner in enumerate(memory.learners):
        if learner.id == learner_id:
            updated_learner.id = learner_id
            memory.learners[i] = updated_learner
            return updated_learner
    return None


def delete_learner(learner_id: int) -> Learner | None:
    for i, learner in enumerate(memory.learners):
        if learner.id == learner_id:
            return memory.learners.pop(i)
    return None
