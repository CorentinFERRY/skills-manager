from fastapi import APIRouter

from skills_manager.routes.learner_routes import router as learner_router
from skills_manager.routes.skill_routes import router as skill_router
from skills_manager.routes.validation_routes import router as validation_router

main_router = APIRouter()

main_router.include_router(learner_router)
main_router.include_router(skill_router)
main_router.include_router(validation_router)
