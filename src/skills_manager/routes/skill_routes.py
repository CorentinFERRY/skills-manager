from typing import List

from fastapi import APIRouter, Header, HTTPException

from skills_manager.models.Skill import Skill
from skills_manager.schemas.skill_schema import SkillCreate
from skills_manager.services import skill_service

router = APIRouter()


@router.get("/competences")
def get_all() -> List[Skill]:
    return skill_service.get_all_skills()


@router.get("/competences/{id}")
def get_by_id(id: int) -> Skill:
    skill = skill_service.get_skill_by_id(id)
    if not skill:
        raise HTTPException(status_code=404, detail="Compétence non trouvée !")
    return skill


@router.post("/competences")
def create(body: SkillCreate, x_role: str = Header(...)) -> Skill:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    return skill_service.create_skill(body.name)


@router.put("/competences/{id}")
def update(id: int, body: SkillCreate, x_role: str = Header(...)) -> Skill:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    updated_skill = skill_service.update_skill(id, body)
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Compétence non trouvée !")
    return updated_skill


@router.delete("/competences/{id}")
def delete(id: int, x_role: str = Header(...)) -> None:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    deleted = skill_service.delete_skill(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Compétence non trouvée !")
