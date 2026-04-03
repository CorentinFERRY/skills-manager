from src.models.Validation import Validation
from src.repositories import validation_repository
from src.services.learner_service import get_learner_by_id


def create_validation(learner_id: int, skill_id: int) -> Validation:
    new_validation = validation_repository.insert_validation(learner_id, skill_id)
    return Validation(
        id=new_validation["id"],
        learner_id=new_validation["learner_id"],
        skill_id=new_validation["skill_id"],
        status=new_validation["status"],
    )


def create_pre_validation(
    learner_id: int, skill_id: int, validator_id: int
) -> Validation:
    validator = get_learner_by_id(validator_id)
    if validator is None or not validator.can_validate(skill_id):
        raise ValueError("Le pair n'a pas cette compétence validée")
    new_validation = validation_repository.insert_pre_validation(
        learner_id, skill_id, validator_id
    )
    return Validation(
        id=new_validation["id"],
        learner_id=new_validation["learner_id"],
        skill_id=new_validation["skill_id"],
        status=new_validation["status"],
        pre_validated_by=new_validation["pre_validated_by"],
    )
