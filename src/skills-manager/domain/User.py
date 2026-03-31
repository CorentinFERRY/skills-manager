class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def can_validate(self, skill_id: int) -> bool:
        return False
