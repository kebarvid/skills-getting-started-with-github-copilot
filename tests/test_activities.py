def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_and_unregister_participant(client):
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in signup_response.json()["message"]

    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200
    assert email in unregister_response.json()["message"]

    updated_activity = client.get("/activities").json()[activity_name]
    assert email not in updated_activity["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    response = client.post("/activities/NotARealClub/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_nonexistent_activity_returns_404(client):
    response = client.delete("/activities/NotARealClub/unregister?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_400(client):
    activity_name = "Chess Club"
    email = "not-signed-up@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"