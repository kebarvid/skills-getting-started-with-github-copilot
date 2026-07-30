from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in response.json()["message"]

    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200
    assert email in unregister_response.json()["message"]

    updated_activity = client.get("/activities").json()[activity_name]
    assert email not in updated_activity["participants"]
