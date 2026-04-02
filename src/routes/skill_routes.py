from typing import List

from fastapi import APIRouter, Header, HTTPException

from src.schemas.skill_schema import SkillCreate, SkillResponse
from src.services import skill_service

router = APIRouter()


@router.get("/competences")
def get_all() -> List[SkillResponse]:
    skills = skill_service.get_all_skills()
    return [SkillResponse(id=skill.id, name=skill.name) for skill in skills]


@router.get("/competences/{id}")
def get_by_id(id: int) -> SkillResponse:
    skill = skill_service.get_skill_by_id(id)
    if not skill:
        raise HTTPException(status_code=404, detail="Compétence non trouvée !")
    return SkillResponse(id=skill.id, name=skill.name)


@router.post("/competences", status_code=201)
def create(body: SkillCreate, x_role: str = Header(...)) -> SkillResponse:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    skill = skill_service.create_skill(body.name)
    return SkillResponse(id=skill.id, name=skill.name)


@router.put("/competences/{id}")
def update(id: int, body: SkillCreate, x_role: str = Header(...)) -> SkillResponse:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    updated_skill = skill_service.update_skill(id, body)
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Compétence non trouvée !")
    return SkillResponse(id=updated_skill.id, name=updated_skill.name)


@router.delete("/competences/{id}", status_code=204)
def delete(id: int, x_role: str = Header(...)) -> None:
    if x_role != "trainer":
        raise HTTPException(status_code=403, detail="Réservé aux formateurs")
    deleted = skill_service.delete_skill(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Compétence non trouvée !")
