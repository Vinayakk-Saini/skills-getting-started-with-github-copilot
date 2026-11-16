from src.app import activities


ACTIVITY_NAME = "Chess Club"


def test_root_redirects_to_activity_page(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json()[ACTIVITY_NAME]["participants"] == activities[ACTIVITY_NAME]["participants"]


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {ACTIVITY_NAME}"}
    assert email in activities[ACTIVITY_NAME]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = activities[ACTIVITY_NAME]["participants"][0]

    response = client.post(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_not_found_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_removes_participant(client):
    email = activities[ACTIVITY_NAME]["participants"][0]

    response = client.delete(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {ACTIVITY_NAME}"}
    assert email not in activities[ACTIVITY_NAME]["participants"]


def test_delete_returns_not_found_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_returns_not_found_for_unregistered_participant(client):
    response = client.delete(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": "unregistered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
