import sqlite3
from typing import Any, AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from src.database.database import init_db, set_connection
from src.main import app
from src.schemas.learner_schema import LearnerCreate
from src.schemas.skill_schema import SkillCreate
from src.schemas.trainer_schema import TrainerCreate
from src.schemas.validation_schema import (
    PreValidationCreate,
    ValidationCreate,
)

# --- Réinitialisation de la DB entre chaque test ---


@pytest.fixture(autouse=True)
async def reset_db() -> AsyncGenerator[None, None]:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    init_db(conn)
    set_connection(conn)
    yield
    conn.close()


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
    learner_headers: dict[str, str],
    trainer_headers: dict[str, str],
) -> dict[str, Any]:
    # setup : créer le validator avec la compétence validée via les routes
    await client.post("/apprenants", json={"name": "Bob"}, headers=trainer_headers)
    await client.post("/competences", json={"name": "Python"}, headers=trainer_headers)
    await client.post(
        "/validations",
        json={"learner_id": 1, "skill_id": 1},
        headers=trainer_headers,
    )
    response = await client.post(
        "/pre-validations",
        json={"learner_id": 2, "skill_id": 1, "validator_id": 1},
        headers=learner_headers,
    )
    return response.json()
