import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def client():
    # Use a fresh client for each test
    return TestClient(app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow(client):
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure email not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Signup same email again should return 400
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Unregister
    resp3 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp3.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregister again should be 400
    resp4 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp4.status_code == 400


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/Nonexistent/signup?email=x@example.com")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity(client):
    resp = client.delete("/activities/Nonexistent/unregister?email=x@example.com")
    assert resp.status_code == 404
