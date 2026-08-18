"""Tests for GET /activities endpoint using AAA pattern."""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, test_client):
        """Test that GET /activities returns all activities.
        
        Arrange: Test client ready with fresh activities
        Act: Send GET request to /activities
        Assert: Verify response is 200 with all activities present
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Team",
            "Science Club",
        ]

        # Act
        response = test_client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_response_structure(self, test_client):
        """Test that GET /activities returns correct JSON structure.
        
        Arrange: Test client ready
        Act: Send GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = test_client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
            # Verify field types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participant_counts(self, test_client):
        """Test that participant counts match expected values.
        
        Arrange: Test client ready
        Act: Send GET request to /activities
        Assert: Verify specific activities have correct participant counts
        """
        # Arrange
        expected_counts = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
            "Basketball Team": 1,
            "Tennis Club": 2,
            "Art Studio": 1,
            "Music Ensemble": 3,
            "Debate Team": 1,
            "Science Club": 2,
        }

        # Act
        response = test_client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, expected_count in expected_counts.items():
            actual_count = len(activities[activity_name]["participants"])
            assert actual_count == expected_count, (
                f"{activity_name} has {actual_count} participants, "
                f"expected {expected_count}"
            )
