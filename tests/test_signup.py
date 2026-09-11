def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert activities_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_rejects_missing_activity(client):
    # Arrange
    activity_name = "Missing Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_rejects_full_activity(client):
    # Arrange
    activity_name = "Soccer Team"
    emails = [f"student{number}@mergington.edu" for number in range(18)]
    overflow_email = "overflow@mergington.edu"

    # Act
    signup_responses = [
        client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )
        for email in emails
    ]
    overflow_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": overflow_email}
    )

    # Assert
    assert all(response.status_code == 200 for response in signup_responses)
    assert overflow_response.status_code == 400
    assert overflow_response.json() == {"detail": "Activity is full"}