from typing import Any

from httpx import AsyncClient

from src.schemas.validation_schema import PreValidationCreate, ValidationCreate


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
        created_validation: dict[str, Any],
    ) -> None:
        assert created_validation["learner_id"] == 1
        assert created_validation["skill_id"] == 1
        assert created_validation["status"] == "validated"

    async def test_create_validation_without_role_returns_422(
        self,
        client: AsyncClient,
        validation_payload: ValidationCreate,
    ) -> None:
        response = await client.post(
            "/validations",
            json=validation_payload.model_dump(),
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
        created_pre_validation: dict[str, Any],
    ) -> None:
        assert created_pre_validation["status"] == "pre_validated"

    async def test_create_pre_validation_returns_correct_status(
        self,
        client: AsyncClient,
        created_pre_validation: dict[str, Any],
    ) -> None:
        assert created_pre_validation["status"] == "pre_validated"
        assert created_pre_validation["pre_validated_by"] == 1

    async def test_create_pre_validation_without_role_returns_422(
        self,
        client: AsyncClient,
        pre_validation_payload: PreValidationCreate,
    ) -> None:
        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
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
        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403

    async def test_create_pre_validation_validator_missing_skill_returns_403(
        self,
        client: AsyncClient,
        learner_headers: dict[str, str],
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post("/apprenants", json={"name": "Bob"}, headers=trainer_headers)

        response = await client.post(
            "/pre-validations",
            json={"learner_id": 2, "skill_id": 1, "validator_id": 1},
            headers=learner_headers,
        )
        assert response.status_code == 403
