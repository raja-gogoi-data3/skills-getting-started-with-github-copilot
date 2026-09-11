def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert activities_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_rejects_missing_activity(client):
    # Arrange
    activity_name = "Missing Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_rejects_student_not_enrolled(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }


def test_unregistered_student_can_sign_up_again(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    assert signup_response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }