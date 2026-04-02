from typing import Any

from httpx import AsyncClient

from src.schemas.trainer_schema import TrainerCreate


class TestGetTainers:
    async def test_get_trainers_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/formateurs")
        assert response.status_code == 200

    async def test_get_trainers_retruns_empty_list_by_default(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/formateurs")
        assert response.json() == []

    async def test_get_trainers_returns_list_after_creation(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
    ) -> None:
        response = await client.get("/formateurs")
        assert len(response.json()) == 1


class TestCreateTrainer:
    async def test_create_trainer_returns_201(
        self,
        client: AsyncClient,
        trainer_payload: TrainerCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/formateurs", json=trainer_payload.model_dump(), headers=trainer_headers
        )
        assert response.status_code == 201

    async def test_create_trainer_returns_correct_data(
        self,
        client: AsyncClient,
        trainer_payload: TrainerCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/formateurs", json=trainer_payload.model_dump(), headers=trainer_headers
        )
        assert response.json()["name"] == trainer_payload.name
        assert response.json()["id"] == 1

    async def test_create_trainer_without_role_returns_422(
        self, client: AsyncClient, trainer_payload: TrainerCreate
    ) -> None:
        response = await client.post("/formateurs", json=trainer_payload.model_dump())
        assert response.status_code == 422

    async def test_create_trainer_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        trainer_payload: TrainerCreate,
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/formateurs", json=trainer_payload.model_dump(), headers=learner_headers
        )
        assert response.status_code == 403

    async def test_create_trainer_missing_name_returns_422(
        self, client: AsyncClient, trainer_headers: dict[str, str]
    ) -> None:
        response = await client.post("/formateurs", json={}, headers=trainer_headers)
        assert response.status_code == 422


class TestGetTrainerById:
    async def test_get_trainer_by_id_returns_200(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
    ) -> None:
        response = await client.get(f"/formateurs/{created_trainer['id']}")
        assert response.status_code == 200

    async def test_get_trainer_by_id_returns_correct_data(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
    ) -> None:
        response = await client.get(f"/formateurs/{created_trainer['id']}")
        assert response.json()["id"] == created_trainer["id"]
        assert response.json()["name"] == created_trainer["name"]

    async def test_get_trainer_by_id_returns_404_if_not_found(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.get("/formateurs/999")
        assert response.status_code == 404


class TestUpdateTrainer:
    async def test_update_trainer_returns_200(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.put(
            f"/formateurs/{created_trainer['id']}",
            json={"name": "Updated Name"},
            headers=trainer_headers,
        )
        assert response.status_code == 200

    async def test_update_trainer_returns_correct_data(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.put(
            f"/formateurs/{created_trainer['id']}",
            json={"name": "Updated Name"},
            headers=trainer_headers,
        )
        assert response.json()["name"] == "Updated Name"
        assert response.json()["id"] == created_trainer["id"]

    async def test_update_trainer_returns_404_if_not_found(
        self,
        client: AsyncClient,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.put(
            "/formateurs/999",
            json={"name": "Updated Name"},
            headers=trainer_headers,
        )
        assert response.status_code == 404

    async def test_update_trainer_missing_name_returns_422(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.put(
            f"/formateurs/{created_trainer['id']}",
            json={},
            headers=trainer_headers,
        )
        assert response.status_code == 422

    async def test_update_trainer_without_role_returns_422(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
    ) -> None:
        response = await client.put(
            f"/formateurs/{created_trainer['id']}",
            json={"name": "Updated Name"},
        )
        assert response.status_code == 422

    async def test_update_trainer_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.put(
            f"/formateurs/{created_trainer['id']}",
            json={"name": "Updated Name"},
            headers=learner_headers,
        )
        assert response.status_code == 403


class TestDeleteTrainer:
    async def test_delete_trainer_returns_204(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.delete(
            f"/formateurs/{created_trainer['id']}", headers=trainer_headers
        )
        assert response.status_code == 204

    async def test_delete_trainer_removes_from_db(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        await client.delete(
            f"/formateurs/{created_trainer['id']}", headers=trainer_headers
        )
        response = await client.get(f"/formateurs/{created_trainer['id']}")
        assert response.status_code == 404

    async def test_delete_trainer_without_role_returns_422(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
    ) -> None:
        response = await client.delete(f"/formateurs/{created_trainer['id']}")
        assert response.status_code == 422

    async def test_delete_trainer_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        created_trainer: dict[str, Any],
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.delete(
            f"/formateurs/{created_trainer['id']}", headers=learner_headers
        )
        assert response.status_code == 403

    async def test_delete_trainer_returns_404_if_not_found(
        self,
        client: AsyncClient,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.delete("/formateurs/999", headers=trainer_headers)
        assert response.status_code == 404
