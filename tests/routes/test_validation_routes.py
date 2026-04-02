from httpx import AsyncClient

from src.database import memory as db
from src.models.Learner import Learner
from src.schemas.validation_schema import (
    PreValidationCreate,
    ValidationCreate,
)


class TestCreateValidation:
    async def test_create_validation_returns_201(
        self,
        client: AsyncClient,
        validation_payload: ValidationCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/validations",
            json=validation_payload.model_dump(),
            headers=trainer_headers,
        )
        assert response.status_code == 201

    async def test_create_validation_returns_correct_data(
        self,
        client: AsyncClient,
        validation_payload: ValidationCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/validations",
            json=validation_payload.model_dump(),
            headers=trainer_headers,
        )
        data = response.json()
        assert data["learner_id"] == validation_payload.learner_id
        assert data["skill_id"] == validation_payload.skill_id
        assert data["status"] == "validated"

    async def test_create_validation_without_role_returns_422(
        self, client: AsyncClient, validation_payload: ValidationCreate
    ) -> None:
        response = await client.post(
            "/validations", json=validation_payload.model_dump()
        )
        assert response.status_code == 422

    async def test_create_validation_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        validation_payload: ValidationCreate,
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/validations",
            json=validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403


class TestCreatePreValidation:
    async def test_create_pre_validation_returns_201(
        self,
        client: AsyncClient,
        pre_validation_payload: PreValidationCreate,
        learner_headers: dict[str, str],
    ) -> None:
        # setup : validator avec la compétence
        validator = Learner(id=2, name="Bob")
        validator.add_validated_skill(1)
        db.learners.append(validator)

        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 201

    async def test_create_pre_validation_returns_correct_status(
        self,
        client: AsyncClient,
        pre_validation_payload: PreValidationCreate,
        learner_headers: dict[str, str],
    ) -> None:
        validator = Learner(id=2, name="Bob")
        validator.add_validated_skill(1)
        db.learners.append(validator)

        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.json()["status"] == "pre_validated"
        assert response.json()["pre_validated_by"] == 2

    async def test_create_pre_validation_without_role_returns_422(
        self, client: AsyncClient, pre_validation_payload: PreValidationCreate
    ) -> None:
        response = await client.post(
            "/pre-validations", json=pre_validation_payload.model_dump()
        )
        assert response.status_code == 422

    async def test_create_pre_validation_with_trainer_role_returns_403(
        self,
        client: AsyncClient,
        pre_validation_payload: PreValidationCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=trainer_headers,
        )
        assert response.status_code == 403

    async def test_create_pre_validation_validator_not_found_returns_403(
        self,
        client: AsyncClient,
        pre_validation_payload: PreValidationCreate,
        learner_headers: dict[str, str],
    ) -> None:
        # DB vide → validator_id=2 n'existe pas
        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403

    async def test_create_pre_validation_validator_missing_skill_returns_403(
        self,
        client: AsyncClient,
        pre_validation_payload: PreValidationCreate,
        learner_headers: dict[str, str],
    ) -> None:
        # validator existe mais n'a pas la compétence
        validator = Learner(id=2, name="Bob")
        db.learners.append(validator)

        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403
