from typing import List

import skills_manager.database.memory as memory
from skills_manager.models.Skill import Skill


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


def update_skill(skill_id: int, updated_skill: Skill) -> Skill | None:
    for i, skill in enumerate(memory.skills):
        if skill.id == skill_id:
            updated_skill.id = skill_id
            memory.skills[i] = updated_skill
            return updated_skill
    return None
