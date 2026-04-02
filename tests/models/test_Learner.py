import pytest

from src.models.Learner import Learner
from src.models.User import User


class TestLearner:
    def test_learner_inherits_from_user(self) -> None:
        learner = Learner(id=5, name="Carol")
        assert isinstance(learner, User)

    def test_learner_attributes(self) -> None:
        learner = Learner(id=5, name="Carol")
        assert learner.id == 5
        assert learner.name == "Carol"

    def test_can_validate_returns_false_initially(self) -> None:
        learner = Learner(id=5, name="Carol")
        assert learner.can_validate(skill_id=1) is False

    def test_can_validate_returns_true_after_adding_skill(self) -> None:
        learner = Learner(id=5, name="Carol")
        learner.add_validated_skill(1)
        assert learner.can_validate(skill_id=1) is True

    def test_can_validate_returns_false_for_unvalidated_skill(self) -> None:
        learner = Learner(id=5, name="Carol")
        learner.add_validated_skill(1)
        assert learner.can_validate(skill_id=2) is False

    def test_add_multiple_skills(self) -> None:
        learner = Learner(id=5, name="Carol")
        learner.add_validated_skill(1)
        learner.add_validated_skill(2)
        learner.add_validated_skill(3)
        assert learner.can_validate(1) is True
        assert learner.can_validate(2) is True
        assert learner.can_validate(3) is True

    def test_add_duplicate_skill_raises_value_error(self) -> None:
        learner = Learner(id=5, name="Carol")
        learner.add_validated_skill(1)
        with pytest.raises(ValueError, match="déja validée"):
            learner.add_validated_skill(1)

    def test_validated_skills_are_private(self) -> None:
        """Les compétences validées ne sont pas accessibles directement."""
        learner = Learner(id=5, name="Carol")
        # L'attribut privé name-mangled ne doit pas être accessible simplement
        assert not hasattr(learner, "_validated_skills")
        assert not hasattr(learner, "validated_skills")

    def test_str_representation(self) -> None:
        learner = Learner(id=5, name="Carol")
        assert str(learner) == "Learner(id=5, name=Carol)"
