import pytest

import skills_manager.database.memory as db
from skills_manager.models.Learner import Learner
from skills_manager.services.validation_service import (
    create_pre_validation,
    create_validation,
)


class TestCreateValidation:
    def test_returns_validation_with_correct_status(self) -> None:
        result = create_validation(learner_id=1, skill_id=1)
        assert result.status == "validated"

    def test_returns_validation_with_correct_ids(self) -> None:
        result = create_validation(learner_id=1, skill_id=2)
        assert result.learner_id == 1
        assert result.skill_id == 2

    def test_increments_id_on_each_creation(self) -> None:
        v1 = create_validation(learner_id=1, skill_id=1)
        v2 = create_validation(learner_id=2, skill_id=1)
        assert v1.id == 1
        assert v2.id == 2

    def test_saves_validation_in_db(self) -> None:
        create_validation(learner_id=1, skill_id=1)
        assert len(db.validations) == 1


class TestCreatePreValidation:
    def test_raises_if_validator_not_found(self) -> None:
        with pytest.raises(ValueError, match="compétence validée"):
            create_pre_validation(learner_id=1, skill_id=1, validator_id=99)

    def test_raises_if_validator_does_not_have_skill(self) -> None:
        validator = Learner(id=2, name="Bob")
        db.learners.append(validator)  # pas de compétence ajoutée

        with pytest.raises(ValueError, match="compétence validée"):
            create_pre_validation(learner_id=1, skill_id=1, validator_id=2)

    def test_returns_pre_validation_with_correct_status(self) -> None:
        validator = Learner(id=2, name="Bob")
        validator.add_validated_skill(1)
        db.learners.append(validator)

        result = create_pre_validation(learner_id=1, skill_id=1, validator_id=2)
        assert result.status == "pre_validated"

    def test_returns_pre_validation_with_validator_name(self) -> None:
        validator = Learner(id=2, name="Bob")
        validator.add_validated_skill(1)
        db.learners.append(validator)

        result = create_pre_validation(learner_id=1, skill_id=1, validator_id=2)
        assert result.pre_validated_by == "Bob"

    def test_saves_pre_validation_in_db(self) -> None:
        validator = Learner(id=2, name="Bob")
        validator.add_validated_skill(1)
        db.learners.append(validator)

        create_pre_validation(learner_id=1, skill_id=1, validator_id=2)
        assert len(db.validations) == 1
