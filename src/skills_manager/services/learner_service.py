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
