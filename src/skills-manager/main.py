from domain.Learner import Learner
from domain.Promotion import Promotion
from domain.Skill import Skill
from domain.Trainer import Trainer
from domain.Validation import Validation


def main():
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
