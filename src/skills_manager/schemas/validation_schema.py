from pydantic import BaseModel


class ValidationCreate(BaseModel):
    learner_id: int
    skill_id: int


class PreValidationCreate(BaseModel):
    learner_id: int  # l'apprenant à pré-valider
    skill_id: int
    validator_id: int  # l'apprenant qui pré-valide (doit avoir la compétence)
