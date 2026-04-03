import pytest

from src.models.Validation import Validation
from src.repositories import learner_repository, validation_repository
from src.services.validation_service import create_pre_validation, create_validation


class TestCreateValidation:
    def test_returns_validation_with_correct_status(self) -> None:
        result: Validation = create_validation(learner_id=1, skill_id=1)
        assert result.status == "validated"

    def test_returns_validation_with_correct_ids(self) -> None:
        result: Validation = create_validation(learner_id=1, skill_id=2)
        assert result.learner_id == 1
        assert result.skill_id == 2

    def test_increments_id_on_each_creation(self) -> None:
        v1: Validation = create_validation(learner_id=1, skill_id=1)
        v2: Validation = create_validation(learner_id=2, skill_id=1)
        assert v1.id != v2.id

    def test_saves_validation_in_db(self) -> None:
        create_validation(learner_id=1, skill_id=1)
        rows = validation_repository.find_validated_skills_by_learner(1)
        assert len(rows) == 1


class TestCreatePreValidation:
    def test_raises_if_validator_not_found(self) -> None:
        with pytest.raises(ValueError, match="compétence validée"):
            create_pre_validation(learner_id=1, skill_id=1, validator_id=99)

    def test_raises_if_validator_does_not_have_skill(self) -> None:
        learner_repository.insert("Bob")  # id=1 — pas de compétence ajoutée

        with pytest.raises(ValueError, match="compétence validée"):
            create_pre_validation(learner_id=1, skill_id=1, validator_id=1)

    def test_returns_pre_validation_with_correct_status(self) -> None:
        learner_repository.insert("Bob")  # id=1
        validation_repository.insert_validation(
            learner_id=1, skill_id=1
        )  # Bob a la compétence 1

        result: Validation = create_pre_validation(
            learner_id=2, skill_id=1, validator_id=1
        )
        assert result.status == "pre_validated"

    def test_returns_pre_validation_with_validator_id(self) -> None:
        learner_repository.insert("Bob")  # id=1
        validation_repository.insert_validation(learner_id=1, skill_id=1)

        result: Validation = create_pre_validation(
            learner_id=2, skill_id=1, validator_id=1
        )
        assert result.pre_validated_by is not None
        assert result.pre_validated_by == 1

    def test_saves_pre_validation_in_db(self) -> None:
        learner_repository.insert("Bob")  # id=1
        validation_repository.insert_validation(learner_id=1, skill_id=1)

        create_pre_validation(learner_id=2, skill_id=1, validator_id=1)
        rows = validation_repository.find_validated_skills_by_learner(2)
        assert (
            len(rows) == 0
        )  # pre_validated != validated, donc pas dans find_validated_skills
