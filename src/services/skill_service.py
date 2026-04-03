from typing import List

from src.models.Skill import Skill
from src.repositories import skill_repository
from src.schemas.skill_schema import SkillCreate


def get_all_skills() -> List[Skill]:
    skills = skill_repository.find_all()
    return [Skill(id=skill["id"], name=skill["name"]) for skill in skills]


def get_skill_by_id(skill_id: int) -> Skill | None:
    skill = skill_repository.find_by_id(skill_id)
    if not skill:
        return None
    return Skill(id=skill["id"], name=skill["name"])


def create_skill(name: str) -> Skill:
    skill_id = skill_repository.insert(name)
    return Skill(id=skill_id, name=name)


def update_skill(skill_id: int, data: SkillCreate) -> Skill | None:
    updated = skill_repository.update(skill_id, data.name)
    if not updated:
        return None
    return Skill(id=skill_id, name=data.name)


def delete_skill(skill_id: int) -> bool:
    return skill_repository.delete(skill_id)
