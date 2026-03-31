from dataclasses import dataclass


@dataclass
class Skill:
    id: int
    name: str

    @staticmethod
    def create(id: int, name: str) -> "Skill":
        return Skill(id, name)
