from .User import User


class Trainer(User):
    def can_validate(self, skill_id: int) -> bool:
        return True

    def __str__(self) -> str:
        return f"Trainer(id={self.id}, name={self.name})"
