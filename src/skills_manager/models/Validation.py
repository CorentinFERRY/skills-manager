from dataclasses import dataclass


@dataclass
class Validation:
    id: int
    learner_id: int
    skill_id: int
    status: str
    pre_validated_by: int | None = None
