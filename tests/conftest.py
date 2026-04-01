from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient

import skills_manager.database.memory as db
from skills_manager.main import app
from skills_manager.schemas.learner_schema import LearnerCreate
from skills_manager.schemas.skill_schema import SkillCreate
from skills_manager.schemas.validation_schema import (
    PreValidationCreate,
    ValidationCreate,
)


# --- Réinitialisation de la DB entre chaque test ---
@pytest.fixture(autouse=True)
def reset_db() -> Generator[None, None, None]:
    db.learners.clear()
    db.skills.clear()
    db.validations.clear()
    db.current_learner_id = 1
    db.current_skill_id = 1
    db.current_validation_id = 1
    yield


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


# --- Headers ---
@pytest.fixture
def trainer_headers() -> dict[str, str]:
    return {"x-role": "trainer"}  # Pour les routes réservées aux formateurs


@pytest.fixture
def learner_headers() -> dict[str, str]:
    return {"x-role": "learner"}  # Pour les routes réservées aux apprenants


# --- Payloads ---
@pytest.fixture
def learner_payload() -> LearnerCreate:
    return LearnerCreate(name="Test User")


@pytest.fixture
def skill_payload() -> SkillCreate:
    return SkillCreate(name="Test Skill")


@pytest.fixture
def validation_payload() -> ValidationCreate:
    return ValidationCreate(learner_id=1, skill_id=1)


@pytest.fixture
def pre_validation_payload() -> PreValidationCreate:
    return PreValidationCreate(learner_id=1, skill_id=1, validator_id=2)
