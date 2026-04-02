from typing import List

import src.database.memory as memory
from src.models.Skill import Skill
from src.schemas.skill_schema import SkillCreate


def get_all_skills() -> List[Skill]:
    return memory.skills


def get_skill_by_id(skill_id: int) -> Skill | None:
    for skill in memory.skills:
        if skill.id == skill_id:
            return skill
    return None


def create_skill(name: str) -> Skill:
    new_skill = Skill(id=memory.current_skill_id, name=name)
    memory.current_skill_id += 1
    memory.skills.append(new_skill)
    return new_skill


def update_skill(skill_id: int, data: SkillCreate) -> Skill | None:
    for i, skill in enumerate(memory.skills):
        if skill.id == skill_id:
            skill.name = data.name
            return skill
    return None


def delete_skill(skill_id: int) -> Skill | None:
    for i, skill in enumerate(memory.skills):
        if skill.id == skill_id:
            return memory.skills.pop(i)
    return None
