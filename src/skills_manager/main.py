from fastapi import FastAPI

from skills_manager.models.Learner import Learner
from skills_manager.models.Promotion import Promotion
from skills_manager.models.Skill import Skill
from skills_manager.models.Trainer import Trainer
from skills_manager.models.Validation import Validation
from skills_manager.routes.main_router import main_router

app = FastAPI()

app.include_router(main_router)


def main() -> None:
    test_user1 = Learner(1, "Corentin")
    print(test_user1)
    test_user2 = Trainer(2, "Paul")
    print(test_user2)

    p1 = Promotion()
    p1.add_user(test_user1)
    p2 = Promotion()
    p2.add_user(test_user2)
    p2026 = p1 + p2
    print(p2026.users[0])
    print(p2026.users[1])

    c1 = Skill(1, "Python")
    c2 = Skill(2, "Java")
    c3 = Skill(3, "C++")

    print(c1)
    print(c2)
    print(c3)

    test_user1.add_validated_skill(c1.id)

    v1 = Validation(1, test_user1.id, c1.id, "Validated", test_user2.name)
    print(v1)


if __name__ == "__main__":
    main()
