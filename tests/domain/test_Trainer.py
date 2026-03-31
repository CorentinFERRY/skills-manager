from skills_manager.domain.Trainer import Trainer
from skills_manager.domain.User import User


class TestTrainer:
    def test_trainer_inherits_from_user(self) -> None:
        trainer = Trainer(id=10, name="Bob")
        assert isinstance(trainer, User)

    def test_trainer_attributes(self) -> None:
        trainer = Trainer(id=10, name="Bob")
        assert trainer.id == 10
        assert trainer.name == "Bob"

    def test_can_validate_returns_true(self) -> None:
        trainer = Trainer(id=10, name="Bob")
        assert trainer.can_validate(skill_id=1) is True

    def test_can_validate_always_true_regardless_of_skill(self) -> None:
        trainer = Trainer(id=10, name="Bob")
        for skill_id in [0, 1, 99, -1]:
            assert trainer.can_validate(skill_id) is True

    def test_str_representation(self) -> None:
        trainer = Trainer(id=10, name="Bob")
        assert str(trainer) == "Trainer(id=10, name=Bob)"
