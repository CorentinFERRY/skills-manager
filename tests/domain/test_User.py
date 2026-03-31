from domain.User import User


class TestUser:
    def test_creation(self):
        user = User(id=1, name="Alice")
        assert user.id == 1
        assert user.name == "Alice"

    def test_can_validate_returns_false(self):
        user = User(id=1, name="Alice")
        assert user.can_validate(skill_id=42) is False

    def test_can_validate_always_false_regardless_of_skill(self):
        user = User(id=1, name="Alice")
        for skill_id in [0, 1, 99, -1]:
            assert user.can_validate(skill_id) is False
