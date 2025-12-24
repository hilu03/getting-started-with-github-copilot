from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    activity = "Chess Club"
    email = "testuser@example.test"

    # sign up
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    # duplicate signup should fail
    resp2 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp2.status_code == 400
    assert "Student already signed up" in resp2.json().get("detail", "")


def test_unregister(client):
    activity = "Chess Club"
    email = "toremove@example.test"

    # ensure user is signed up first
    r1 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert r1.status_code == 200

    # unregister
    r2 = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert r2.status_code == 200
    assert f"Unregistered {email}" in r2.json().get("message", "")

    # trying again should return 404
    r3 = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert r3.status_code == 404


def test_unregister_nonexistent_activity(client):
    r = client.delete("/activities/NoSuchActivity/participants?email=foo@bar")
    assert r.status_code == 404
