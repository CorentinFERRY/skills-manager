from domain.User import User


class Promotion:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.users = []  # Liste d'objets User

    def add_user(self, user: User) -> None:
        if isinstance(user, User):
            self.users.append(user)
        else:
            raise TypeError("Seuls les objets User sont acceptés")
