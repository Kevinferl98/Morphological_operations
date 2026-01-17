from tests.utils.api_helpers import submit_job

def test_create_job_ok(client):
    response = submit_job(client)

    assert response.status_code == 202

    data = response.json
    assert "job_id" in data
    assert isinstance(data["job_id"], str)