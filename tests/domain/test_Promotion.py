import pytest
from domain.Learner import Learner
from domain.Promotion import Promotion
from domain.Trainer import Trainer
from domain.User import User


class TestPromotion:
    def test_creation_empty(self):
        promo = Promotion()
        assert promo.users == []

    def test_add_user(self):
        promo = Promotion()
        user = User(id=1, name="Alice")
        promo.add_user(user)
        assert len(promo.users) == 1
        assert promo.users[0] is user

    def test_add_trainer(self):
        promo = Promotion()
        trainer = Trainer(id=10, name="Bob")
        promo.add_user(trainer)
        assert len(promo.users) == 1

    def test_add_learner(self):
        promo = Promotion()
        learner = Learner(id=5, name="Carol")
        promo.add_user(learner)
        assert len(promo.users) == 1

    def test_add_non_user_raises_type_error(self):
        promo = Promotion()
        with pytest.raises(TypeError, match="User"):
            promo.add_user("pas un user")  # type: ignore

    def test_add_non_user_integer_raises_type_error(self):
        promo = Promotion()
        with pytest.raises(TypeError):
            promo.add_user(42)  # type: ignore

    def test_add_multiple_users(self):
        promo = Promotion()
        for i in range(5):
            promo.add_user(User(id=i, name=f"User{i}"))
        assert len(promo.users) == 5

    def test_merge_two_promotions(self):
        promo1 = Promotion()
        promo1.add_user(User(id=1, name="Alice"))
        promo2 = Promotion()
        promo2.add_user(User(id=2, name="Bob"))

        merged = promo1 + promo2
        assert isinstance(merged, Promotion)
        assert len(merged.users) == 2

    def test_merge_preserves_original_promotions(self):
        promo1 = Promotion()
        promo1.add_user(User(id=1, name="Alice"))
        promo2 = Promotion()
        promo2.add_user(User(id=2, name="Bob"))

        _ = promo1 + promo2
        assert len(promo1.users) == 1
        assert len(promo2.users) == 1

    def test_merge_with_non_promotion_returns_not_implemented(self):
        promo = Promotion()
        result = promo.__add__("pas une promo")  # type: ignore
        assert result is NotImplemented

    def test_merge_empty_promotions(self):
        promo1 = Promotion()
        promo2 = Promotion()
        merged = promo1 + promo2
        assert len(merged.users) == 0