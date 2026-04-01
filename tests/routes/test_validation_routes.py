import skills_manager.database.memory as db
from skills_manager.models.Learner import Learner


class TestCreateValidation:
    async def test_create_validation_returns_201(
        self, client, validation_payload, trainer_headers
    ):
        response = await client.post(
            "/validations",
            json=validation_payload.model_dump(),
            headers=trainer_headers,
        )
        assert response.status_code == 201

    async def test_create_validation_returns_correct_data(
        self, client, validation_payload, trainer_headers
    ):
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
        self, client, validation_payload
    ):
        response = await client.post(
            "/validations", json=validation_payload.model_dump()
        )
        assert response.status_code == 422

    async def test_create_validation_with_learner_role_returns_403(
        self, client, validation_payload, learner_headers
    ):
        response = await client.post(
            "/validations",
            json=validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403


class TestCreatePreValidation:
    async def test_create_pre_validation_returns_201(
        self, client, pre_validation_payload, learner_headers
    ):
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
        self, client, pre_validation_payload, learner_headers
    ):
        validator = Learner(id=2, name="Bob")
        validator.add_validated_skill(1)
        db.learners.append(validator)

        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.json()["status"] == "pre_validated"
        assert response.json()["pre_validated_by"] == "Bob"

    async def test_create_pre_validation_without_role_returns_422(
        self, client, pre_validation_payload
    ):
        response = await client.post(
            "/pre-validations", json=pre_validation_payload.model_dump()
        )
        assert response.status_code == 422

    async def test_create_pre_validation_with_trainer_role_returns_403(
        self, client, pre_validation_payload, trainer_headers
    ):
        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=trainer_headers,
        )
        assert response.status_code == 403

    async def test_create_pre_validation_validator_not_found_returns_403(
        self, client, pre_validation_payload, learner_headers
    ):
        # DB vide → validator_id=2 n'existe pas
        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403

    async def test_create_pre_validation_validator_missing_skill_returns_403(
        self, client, pre_validation_payload, learner_headers
    ):
        # validator existe mais n'a pas la compétence
        validator = Learner(id=2, name="Bob")
        db.learners.append(validator)

        response = await client.post(
            "/pre-validations",
            json=pre_validation_payload.model_dump(),
            headers=learner_headers,
        )
        assert response.status_code == 403
