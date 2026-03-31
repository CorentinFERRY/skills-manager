class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def can_validate(self, skill_id: int) -> bool:
        return False

    def __str__(self) -> str:
        return f"User(id={self.id}, name={self.name})"
