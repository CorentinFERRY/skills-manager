from fastapi import APIRouter, Header, HTTPException

from src.schemas.validation_schema import (
    PreValidationCreate,
    ValidationCreate,
    ValidationResponse,
)
from src.services.validation_service import (
    create_pre_validation,
    create_validation,
)

router = APIRouter()


@router.post("/validations", status_code=201)
def validate_skill(
    body: ValidationCreate, x_role: str = Header(...)
) -> ValidationResponse:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    validation = create_validation(body.learner_id, body.skill_id)
    return ValidationResponse.from_model(validation)


@router.post("/pre-validations", status_code=201)
def pre_validate_skill(
    body: PreValidationCreate, x_role: str = Header(...)
) -> ValidationResponse:
    if x_role != "learner":
        raise HTTPException(status_code=403, detail="Réservé aux apprenants")
    try:
        validation = create_pre_validation(
            body.learner_id, body.skill_id, body.validator_id
        )
        return ValidationResponse.from_model(validation)

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
