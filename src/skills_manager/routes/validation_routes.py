from fastapi import APIRouter, Header, HTTPException

from skills_manager.models.Validation import Validation
from skills_manager.schemas.validation_schema import (
    PreValidationCreate,
    ValidationCreate,
)
from skills_manager.services.validation_service import (
    create_pre_validation,
    create_validation,
)

router = APIRouter()


@router.post("/validations", status_code=201)
def validate_skill(body: ValidationCreate, x_role: str = Header(...)) -> Validation:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    return create_validation(body.learner_id, body.skill_id)


@router.post("/pre-validations", status_code=201)
def pre_validate_skill(
    body: PreValidationCreate, x_role: str = Header(...)
) -> Validation:
    if x_role != "learner":
        raise HTTPException(status_code=403, detail="Réservé aux apprenants")
    try:
        return create_pre_validation(body.learner_id, body.skill_id, body.validator_id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
