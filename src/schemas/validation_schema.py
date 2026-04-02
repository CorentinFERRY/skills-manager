from pydantic import BaseModel

from src.models.Validation import Validation


class ValidationCreate(BaseModel):
    learner_id: int
    skill_id: int


class PreValidationCreate(BaseModel):
    learner_id: int  # l'apprenant à pré-valider
    skill_id: int
    validator_id: int  # l'apprenant qui pré-valide (doit avoir la compétence)


class ValidationResponse(BaseModel):
    id: int
    learner_id: int
    skill_id: int
    status: str
    pre_validated_by: int | None = None

    @classmethod
    def from_model(cls, v: Validation) -> "ValidationResponse":
        return cls(
            id=v.id,
            learner_id=v.learner_id,
            skill_id=v.skill_id,
            status=v.status,
            pre_validated_by=v.pre_validated_by,
        )
