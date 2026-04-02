from httpx import AsyncClient

from src.schemas.skill_schema import SkillCreate


class TestGetSkills:
    async def test_get_skills_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/competences")
        assert response.status_code == 200

    async def test_get_skills_returns_empty_list_by_default(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/competences")
        assert response.json() == []

    async def test_get_skills_returns_list_after_creation(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.get("/competences")
        assert len(response.json()) == 1


class TestGetSkillById:
    async def test_get_skill_by_id_returns_200(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.get("/competences/1")
        assert response.status_code == 200

    async def test_get_skill_by_id_returns_correct_data(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.get("/competences/1")
        assert response.json()["id"] == 1
        assert response.json()["name"] == skill_payload.name

    async def test_get_skill_by_id_returns_404_if_not_found(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.get("/competences/999")
        assert response.status_code == 404


class TestCreateSkill:
    async def test_create_skill_returns_201(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        assert response.status_code == 201

    async def test_create_skill_returns_correct_data(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        assert response.json()["name"] == skill_payload.name
        assert response.json()["id"] == 1

    async def test_create_skill_without_role_returns_422(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
    ) -> None:
        response = await client.post("/competences", json=skill_payload.model_dump())
        assert response.status_code == 422

    async def test_create_skill_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        learner_headers: dict[str, str],
    ) -> None:
        response = await client.post(
            "/competences", json=skill_payload.model_dump(), headers=learner_headers
        )
        assert response.status_code == 403

    async def test_create_skill_missing_name_returns_422(
        self,
        client: AsyncClient,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.post("/competences", json={}, headers=trainer_headers)
        assert response.status_code == 422


class TestUpdateSkill:
    async def test_update_skill_returns_200(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.put(
            "/competences/1", json={"name": "Updated Skill"}, headers=trainer_headers
        )
        assert response.status_code == 200

    async def test_update_skill_returns_correct_data(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.put(
            "/competences/1", json={"name": "Updated Skill"}, headers=trainer_headers
        )
        assert response.json()["name"] == "Updated Skill"
        assert response.json()["id"] == 1

    async def test_update_skill_without_role_returns_422(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.put("/competences/1", json={"name": "Updated Skill"})
        assert response.status_code == 422

    async def test_update_skill_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
        learner_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.put(
            "/competences/1", json={"name": "Updated Skill"}, headers=learner_headers
        )
        assert response.status_code == 403

    async def test_update_skill_returns_404_if_not_found(
        self,
        client: AsyncClient,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.put(
            "/competences/999", json={"name": "Updated Skill"}, headers=trainer_headers
        )
        assert response.status_code == 404


class TestDeleteSkill:
    async def test_delete_skill_returns_204(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.delete("/competences/1", headers=trainer_headers)
        assert response.status_code == 204

    async def test_delete_skill_removes_from_db(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        await client.delete("/competences/1", headers=trainer_headers)
        response = await client.get("/competences/1")
        assert response.status_code == 404

    async def test_delete_skill_without_role_returns_422(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.delete("/competences/1")
        assert response.status_code == 422

    async def test_delete_skill_with_learner_role_returns_403(
        self,
        client: AsyncClient,
        skill_payload: SkillCreate,
        trainer_headers: dict[str, str],
        learner_headers: dict[str, str],
    ) -> None:
        await client.post(
            "/competences", json=skill_payload.model_dump(), headers=trainer_headers
        )
        response = await client.delete("/competences/1", headers=learner_headers)
        assert response.status_code == 403

    async def test_delete_skill_returns_404_if_not_found(
        self,
        client: AsyncClient,
        trainer_headers: dict[str, str],
    ) -> None:
        response = await client.delete("/competences/999", headers=trainer_headers)
        assert response.status_code == 404
