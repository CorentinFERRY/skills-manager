from domain.User import User


class Trainer(User):

    def can_validate(self,skill_id: int)->bool :
        return True