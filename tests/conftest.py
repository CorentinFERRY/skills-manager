from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient

from src.database import memory as db
from src.main import app
from src.models.Learner import Learner
from src.schemas.learner_schema import LearnerCreate
from src.schemas.skill_schema import SkillCreate
from src.schemas.trainer_schema import TrainerCreate
from src.schemas.validation_schema import (
    PreValidationCreate,
    ValidationCreate,
)


# --- Réinitialisation de la DB entre chaque test ---
@pytest.fixture(autouse=True)
def reset_db() -> Generator[None, None, None]:
    db.learners.clear()
    db.skills.clear()
    db.validations.clear()
    db.trainers.clear()
    db.current_learner_id = 1
    db.current_skill_id = 1
    db.current_validation_id = 1
    db.current_trainer_id = 1
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
    return LearnerCreate(name="Test Learner")


@pytest.fixture
def trainer_payload() -> TrainerCreate:
    return TrainerCreate(name="Test Trainer")


@pytest.fixture
def skill_payload() -> SkillCreate:
    return SkillCreate(name="Test Skill")


@pytest.fixture
def validation_payload() -> ValidationCreate:
    return ValidationCreate(learner_id=1, skill_id=1)


@pytest.fixture
def pre_validation_payload() -> PreValidationCreate:
    return PreValidationCreate(learner_id=1, skill_id=1, validator_id=2)


# --- Datas for tests ---


@pytest.fixture
async def created_learner(
    client: AsyncClient,
    learner_payload: LearnerCreate,
    trainer_headers: dict[str, str],
) -> dict[str, Any]:
    response = await client.post(
        "/apprenants", json=learner_payload.model_dump(), headers=trainer_headers
    )
    return response.json()  # retourne {"id": 1, "name": "Test Learner"}


@pytest.fixture
async def created_trainer(
    client: AsyncClient,
    trainer_payload: TrainerCreate,
    trainer_headers: dict[str, str],
) -> dict[str, Any]:
    response = await client.post(
        "/formateurs", json=trainer_payload.model_dump(), headers=trainer_headers
    )
    return response.json()


@pytest.fixture
async def created_skill(
    client: AsyncClient,
    skill_payload: SkillCreate,
    trainer_headers: dict[str, str],
) -> dict[str, Any]:
    response = await client.post(
        "/competences", json=skill_payload.model_dump(), headers=trainer_headers
    )
    return response.json()


@pytest.fixture
async def created_validation(
    client: AsyncClient,
    validation_payload: ValidationCreate,
    trainer_headers: dict[str, str],
) -> dict[str, Any]:
    response = await client.post(
        "/validations", json=validation_payload.model_dump(), headers=trainer_headers
    )
    return response.json()


@pytest.fixture
async def created_pre_validation(
    client: AsyncClient,
    pre_validation_payload: PreValidationCreate,
    learner_headers: dict[str, str],
) -> dict[str, Any]:
    # setup obligatoire — le validator doit exister et avoir la compétence
    validator = Learner(id=2, name="Bob")
    validator.add_validated_skill(1)
    db.learners.append(validator)

    response = await client.post(
        "/pre-validations",
        json=pre_validation_payload.model_dump(),
        headers=learner_headers,
    )
    return response.json()
