from domain.Skill import Skill


class TestSkill:
    def test_creation(self):
        skill = Skill(id=1, name="Python")
        assert skill.id == 1
        assert skill.name == "Python"

    def test_is_dataclass(self):
        """Skill est un dataclass : égalité structurelle."""
        skill1 = Skill(id=1, name="Python")
        skill2 = Skill(id=1, name="Python")
        assert skill1 == skill2

    def test_different_skills_not_equal(self):
        skill1 = Skill(id=1, name="Python")
        skill2 = Skill(id=2, name="Java")
        assert skill1 != skill2

    def test_repr(self):
        skill = Skill(id=1, name="Python")
        assert "1" in repr(skill)
        assert "Python" in repr(skill)
