

class TestGetSkills:
    async def test_get_skills_returns_200(self, client):
        response = await client.get("/competences")
        assert response.status_code == 200

    async def test_get_skills_returns_empty_list_by_default(self, client):
        response = await client.get("/competences")
        assert response.json() == []
