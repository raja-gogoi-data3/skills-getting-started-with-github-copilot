def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_seeded_activity_details(client):
    # Arrange
    expected_activity_count = 9
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    activities = response.json()
    assert len(activities) == expected_activity_count
    assert "Chess Club" in activities
    assert required_fields <= activities["Chess Club"].keys()
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]