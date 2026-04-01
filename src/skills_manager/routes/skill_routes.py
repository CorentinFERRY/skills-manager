from fastapi import APIRouter

from skills_manager.services import skill_service

router = APIRouter()


@router.get("/competences")
def get_skills():
    return skill_service.get_all_skills()
