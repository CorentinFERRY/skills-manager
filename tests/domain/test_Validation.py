from skills_manager.domain.Validation import Validation


class TestValidation:
    def test_creation(self) -> None:
        v = Validation(
            id=1,
            learner_id=5,
            skill_id=10,
            status="pending",
            pre_validated_by="trainer_A",
        )
        assert v.id == 1
        assert v.learner_id == 5
        assert v.skill_id == 10
        assert v.status == "pending"
        assert v.pre_validated_by == "trainer_A"

    def test_is_dataclass_equality(self) -> None:
        v1 = Validation(
            id=1,
            learner_id=5,
            skill_id=10,
            status="pending",
            pre_validated_by="trainer_A",
        )
        v2 = Validation(
            id=1,
            learner_id=5,
            skill_id=10,
            status="pending",
            pre_validated_by="trainer_A",
        )
        assert v1 == v2

    def test_different_status_not_equal(self) -> None:
        v1 = Validation(
            id=1,
            learner_id=5,
            skill_id=10,
            status="pending",
            pre_validated_by="trainer_A",
        )
        v2 = Validation(
            id=1,
            learner_id=5,
            skill_id=10,
            status="validated",
            pre_validated_by="trainer_A",
        )
        assert v1 != v2

    def test_repr_contains_fields(self) -> None:
        v = Validation(
            id=1,
            learner_id=5,
            skill_id=10,
            status="pending",
            pre_validated_by="trainer_A",
        )
        r = repr(v)
        assert "pending" in r
        assert "trainer_A" in r
