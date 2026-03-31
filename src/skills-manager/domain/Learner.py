from domain.User import User


class Learner(User):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.validated_skills: list[int] = []

    def add_skill(self, skill_id: int) -> None:
        if skill_id in self.validated_skills:
            raise ValueError("Compétence déja validée")
        self.validated_skills.append(skill_id)

    def can_validate(self, skill_id: int) -> bool:
        return skill_id in self.validated_skills
