"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_successful_signup(self, test_client, test_email):
        """Test successful signup adds participant to activity.
        
        Arrange: Test client with fresh activities, new email not yet signed up
        Act: Send POST request to signup endpoint
        Assert: Verify response is 200, participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {test_email} for {activity_name}"
        
        # Verify participant was added by checking activities
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert test_email in activities[activity_name]["participants"]

    def test_signup_updates_spot_count(self, test_client, test_email):
        """Test that signup correctly updates available spots.
        
        Arrange: Test client, get initial spot count
        Act: Send POST signup request
        Assert: Verify spots decreased by 1
        """
        # Arrange
        activity_name = "Programming Class"
        initial_response = test_client.get("/activities")
        initial_activities = initial_response.json()
        initial_spots = (
            initial_activities[activity_name]["max_participants"]
            - len(initial_activities[activity_name]["participants"])
        )
        
        # Act
        signup_response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )
        
        # Assert
        assert signup_response.status_code == 200
        updated_response = test_client.get("/activities")
        updated_activities = updated_response.json()
        updated_spots = (
            updated_activities[activity_name]["max_participants"]
            - len(updated_activities[activity_name]["participants"])
        )
        assert updated_spots == initial_spots - 1

    def test_duplicate_signup_returns_400(self, test_client, existing_email):
        """Test that duplicate signup returns 400 error.
        
        Arrange: Test client, email already signed up for Chess Club
        Act: Send POST signup request with same email
        Assert: Verify response is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email},
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, test_client, test_email):
        """Test that signup to nonexistent activity returns 404.
        
        Arrange: Test client, invalid activity name
        Act: Send POST signup request to nonexistent activity
        Assert: Verify response is 404 with "Activity not found"
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_with_url_encoded_activity_name(self, test_client, test_email):
        """Test that signup works with URL-encoded activity names.
        
        Arrange: Test client, activity name with spaces
        Act: Send POST signup request with properly encoded activity name
        Assert: Verify response is 200 and participant added
        """
        # Arrange
        activity_name = "Basketball Team"
        encoded_name = "Basketball%20Team"
        
        # Act
        response = test_client.post(
            f"/activities/{encoded_name}/signup",
            params={"email": test_email},
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert test_email in activities[activity_name]["participants"]
