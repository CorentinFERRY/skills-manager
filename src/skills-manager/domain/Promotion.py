from typing import List

from domain.User import User


class Promotion:
    def __init__(self) -> None:
        self.users: List[User] = []  # Liste d'objets User

    def add_user(self, user: User) -> None:
        if isinstance(user, User):
            self.users.append(user)
        else:
            raise TypeError("Seuls les objets User sont acceptés")

    def __add__(self, other_promo: "Promotion") -> "Promotion":
        if not isinstance(other_promo, Promotion):
            return NotImplemented
        new_promo: Promotion = Promotion()
        new_promo.users = self.users + other_promo.users
        return new_promo
