from typing import Any

from httpx import AsyncClient

from src.schemas.learner_schema import LearnerCreate


class TestGetLearners:
    async def test_get_learners_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/apprenants")
        assert response.status_code == 200

    async def test_get_learners_retruns_empty_list_by_default(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/apprenants")
        assert response.json() == []

    async def test_get_learners_returns_list_after_creation(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.get("/apprenants")
        assert len(response.json()) == 1


class TestCreateLearner:
    async def test_create_learner_returns_201(
        self,
        client: AsyncClient,
        learner_payload: LearnerCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=trainer_headers
        )
        assert response.status_code == 201

    async def test_create_learner_returns_correct_data(
        self,
        client: AsyncClient,
        learner_payload: LearnerCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=trainer_headers
        )
        assert response.json()["name"] == learner_payload.name
        assert response.json()["id"] == 1

    async def test_create_learner_without_role_returns_422(
        self, client: AsyncClient, learner_payload: LearnerCreate
    ) -> None:
        response = await client.post("/apprenants", json=learner_payload.model_dump())
        assert response.status_code == 422

    async def test_create_learner_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        learner_payload: LearnerCreate,
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=learner_headers
        )
        assert response.status_code == 403

    async def test_create_learner_missing_name_returns_422(
        self, client: AsyncClient, trainer_headers: dict[str, str]
    ) -> None:
        response = await client.post("/apprenants", json={}, headers=trainer_headers)
        assert response.status_code == 422


class TestGetLearnerById:
    async def test_get_learner_by_id_returns_200(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.get(f"/apprenants/{created_learner['id']}")
        assert response.status_code == 200

    async def test_get_learner_by_id_returns_correct_data(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.get(f"/apprenants/{created_learner['id']}")
        assert response.json()["id"] == created_learner["id"]
        assert response.json()["name"] == created_learner["name"]

    async def test_get_learner_by_id_returns_404_if_not_found(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.get("/apprenants/999")
        assert response.status_code == 404


class TestUpdateLearner:
    async def test_update_learner_returns_200(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.put(
            f"/apprenants/{created_learner['id']}", json={"name": "Updated Name"}
        )
        assert response.status_code == 200

    async def test_update_learner_returns_correct_data(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.put(
            f"/apprenants/{created_learner['id']}", json={"name": "Updated Name"}
        )
        assert response.json()["name"] == "Updated Name"
        assert response.json()["id"] == created_learner["id"]

    async def test_update_learner_returns_404_if_not_found(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.put("/apprenants/999", json={"name": "Updated Name"})
        assert response.status_code == 404

    async def test_update_learner_missing_name_returns_422(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.put(f"/apprenants/{created_learner['id']}", json={})
        assert response.status_code == 422


class TestDeleteLearner:
    async def test_delete_learner_returns_204(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.delete(
            f"/apprenants/{created_learner['id']}", headers=trainer_headers
        )
        assert response.status_code == 204

    async def test_delete_learner_removes_from_db(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
        trainer_headers: dict[str, str],
    ) -> None:
        await client.delete(
            f"/apprenants/{created_learner['id']}", headers=trainer_headers
        )
        response = await client.get(f"/apprenants/{created_learner['id']}")
        assert response.status_code == 404

    async def test_delete_learner_without_role_returns_422(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
    ) -> None:
        response = await client.delete(f"/apprenants/{created_learner['id']}")
        assert response.status_code == 422

    async def test_delete_learner_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        created_learner: dict[str, Any],
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.delete(
            f"/apprenants/{created_learner['id']}", headers=learner_headers
        )
        assert response.status_code == 403

    async def test_delete_learner_returns_404_if_not_found(
        self,
        client: AsyncClient,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.delete("/apprenants/999", headers=trainer_headers)
        assert response.status_code == 404
