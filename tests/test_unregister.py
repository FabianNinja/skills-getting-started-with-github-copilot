"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern."""

import pytest


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_successful_unregister(self, test_client, existing_email):
        """Test successful unregister removes participant from activity.
        
        Arrange: Test client, email already signed up for Chess Club
        Act: Send DELETE request to unregister endpoint
        Assert: Verify response is 200, participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Verify participant is initially in the activity
        initial_response = test_client.get("/activities")
        initial_activities = initial_response.json()
        assert existing_email in initial_activities[activity_name]["participants"]
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email},
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == (
            f"Unregistered {existing_email} from {activity_name}"
        )
        
        # Verify participant was removed
        updated_response = test_client.get("/activities")
        updated_activities = updated_response.json()
        assert existing_email not in updated_activities[activity_name]["participants"]

    def test_unregister_updates_spot_count(self, test_client, existing_email):
        """Test that unregister correctly updates available spots.
        
        Arrange: Test client, get initial spot count
        Act: Send DELETE unregister request
        Assert: Verify spots increased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        initial_response = test_client.get("/activities")
        initial_activities = initial_response.json()
        initial_spots = (
            initial_activities[activity_name]["max_participants"]
            - len(initial_activities[activity_name]["participants"])
        )
        
        # Act
        unregister_response = test_client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email},
        )
        
        # Assert
        assert unregister_response.status_code == 200
        updated_response = test_client.get("/activities")
        updated_activities = updated_response.json()
        updated_spots = (
            updated_activities[activity_name]["max_participants"]
            - len(updated_activities[activity_name]["participants"])
        )
        assert updated_spots == initial_spots + 1

    def test_unregister_nonexistent_participant_returns_400(self, test_client, test_email):
        """Test that unregistering non-participant returns 400 error.
        
        Arrange: Test client, email not signed up for activity
        Act: Send DELETE unregister request
        Assert: Verify response is 400 with "not signed up" error
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": test_email},
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, test_client, existing_email):
        """Test that unregister from nonexistent activity returns 404.
        
        Arrange: Test client, invalid activity name
        Act: Send DELETE unregister request to nonexistent activity
        Assert: Verify response is 404 with "Activity not found"
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email},
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_with_url_encoded_activity_name(self, test_client, existing_email):
        """Test that unregister works with URL-encoded activity names.
        
        Arrange: Test client, activity name with spaces
        Act: Send DELETE unregister request with properly encoded activity name
        Assert: Verify response is 200 and participant removed
        """
        # Arrange
        activity_name = "Music Ensemble"
        encoded_name = "Music%20Ensemble"
        participant = "noah@mergington.edu"  # In Music Ensemble
        
        # Act
        response = test_client.delete(
            f"/activities/{encoded_name}/unregister",
            params={"email": participant},
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert participant not in activities[activity_name]["participants"]

    def test_unregister_then_signup_same_email(self, test_client, existing_email):
        """Test that user can re-signup after unregistering.
        
        Arrange: Test client, participant already signed up
        Act: Unregister, then sign up again
        Assert: Verify both operations succeed
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act - Unregister
        unregister_response = test_client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email},
        )
        
        # Assert unregister worked
        assert unregister_response.status_code == 200
        
        # Act - Sign up again
        signup_response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email},
        )
        
        # Assert signup worked
        assert signup_response.status_code == 200
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert existing_email in activities[activity_name]["participants"]
