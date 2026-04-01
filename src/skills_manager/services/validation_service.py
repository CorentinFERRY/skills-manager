from skills_manager.database import memory
from skills_manager.models.Validation import Validation
from skills_manager.services.learner_service import get_learner_by_id


def create_validation(learner_id: int, skill_id: int) -> Validation:
    new_validation = Validation(
        id=memory.current_validation_id,
        learner_id=learner_id,
        skill_id=skill_id,
        status="validated",
    )
    memory.current_validation_id += 1
    memory.validations.append(new_validation)
    return new_validation


def create_pre_validation(
    learner_id: int, skill_id: int, validator_id: int
) -> Validation:
    validator = get_learner_by_id(validator_id)
    if validator is None or not validator.can_validate(skill_id):
        raise ValueError("Le pair n'a pas cette compétence validée")
    new_validation = Validation(
        id=memory.current_validation_id,
        learner_id=learner_id,
        skill_id=skill_id,
        status="pre_validated",
        pre_validated_by=validator.name,
    )
    memory.current_validation_id += 1
    memory.validations.append(new_validation)
    return new_validation
