from typing import List

from fastapi import APIRouter

from skills_manager.models.Skill import Skill
from skills_manager.services import skill_service

router = APIRouter()


@router.get("/competences")
def get_skills() -> List[Skill]:
    return skill_service.get_all_skills()
