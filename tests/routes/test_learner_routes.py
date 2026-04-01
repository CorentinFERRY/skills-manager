class TestGetLearners:
    async def test_get_learners_returns_200(self, client):
        response = await client.get("/apprenants")
        assert response.status_code == 200

    async def test_get_learners_retruns_empty_list_by_default(self, client):
        response = await client.get("/apprenants")
        assert response.json() == []

    async def test_get_learners_returns_list_after_creation(
        self, client, learner_payload, trainer_headers
    ):
        await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=trainer_headers
        )
        response = await client.get("/apprenants")
        assert len(response.json()) == 1


class TestCreateLearner:
    async def test_create_learner_returns_201(
        self, client, learner_payload, trainer_headers
    ):
        response = await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=trainer_headers
        )
        assert response.status_code == 201

    async def test_create_learner_returns_correct_data(
        self, client, learner_payload, trainer_headers
    ):
        response = await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=trainer_headers
        )
        assert response.json()["name"] == learner_payload.name
        assert response.json()["id"] == 1

    async def test_create_learner_without_role_returns_422(
        self, client, learner_payload
    ):
        response = await client.post("/apprenants", json=learner_payload.model_dump())
        assert response.status_code == 422

    async def test_create_learner_with_learner_role_returns_403(
        self, client, learner_payload, learner_headers
    ):
        response = await client.post(
            "/apprenants", json=learner_payload.model_dump(), headers=learner_headers
        )
        assert response.status_code == 403

    async def test_create_learner_missing_name_returns_422(
        self, client, trainer_headers
    ):
        response = await client.post("/apprenants", json={}, headers=trainer_headers)
        assert response.status_code == 422
