import pytest

from src.models.Learner import Learner
from src.models.Promotion import Promotion
from src.models.Trainer import Trainer
from src.models.User import User


class TestPromotion:
    def test_creation_empty(self) -> None:
        promo = Promotion()
        assert promo.users == []

    def test_add_user(self) -> None:
        promo = Promotion()
        user = User(id=1, name="Alice")
        promo.add_user(user)
        assert len(promo.users) == 1
        assert promo.users[0] is user

    def test_add_trainer(self) -> None:
        promo = Promotion()
        trainer = Trainer(id=10, name="Bob")
        promo.add_user(trainer)
        assert len(promo.users) == 1

    def test_add_learner(self) -> None:
        promo = Promotion()
        learner = Learner(id=5, name="Carol")
        promo.add_user(learner)
        assert len(promo.users) == 1

    def test_add_non_user_raises_type_error(self) -> None:
        promo = Promotion()
        with pytest.raises(TypeError, match="User"):
            promo.add_user("pas un user")  # type: ignore[arg-type]

    def test_add_non_user_integer_raises_type_error(self) -> None:
        promo = Promotion()
        with pytest.raises(TypeError):
            promo.add_user(42)  # type: ignore[arg-type]

    def test_add_multiple_users(self) -> None:
        promo = Promotion()
        for i in range(5):
            promo.add_user(User(id=i, name=f"User{i}"))
        assert len(promo.users) == 5

    def test_merge_two_promotions(self) -> None:
        promo1 = Promotion()
        promo1.add_user(User(id=1, name="Alice"))
        promo2 = Promotion()
        promo2.add_user(User(id=2, name="Bob"))

        merged = promo1 + promo2
        assert isinstance(merged, Promotion)
        assert len(merged.users) == 2

    def test_merge_preserves_original_promotions(self) -> None:
        promo1 = Promotion()
        promo1.add_user(User(id=1, name="Alice"))
        promo2 = Promotion()
        promo2.add_user(User(id=2, name="Bob"))

        _ = promo1 + promo2
        assert len(promo1.users) == 1
        assert len(promo2.users) == 1

    def test_merge_with_non_promotion_returns_not_implemented(self) -> None:
        promo = Promotion()
        result = promo.__add__("pas une promo")  # type: ignore
        assert result is NotImplemented

    def test_merge_empty_promotions(self) -> None:
        promo1 = Promotion()
        promo2 = Promotion()
        merged = promo1 + promo2
        assert len(merged.users) == 0
