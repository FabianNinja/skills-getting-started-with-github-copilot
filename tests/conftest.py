"""Pytest configuration and shared fixtures for FastAPI tests."""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def fresh_activities():
    """Provide a fresh deep copy of activities for each test.
    
    This ensures test isolation by preventing mutations in one test
    from affecting others.
    """
    return copy.deepcopy(activities)


@pytest.fixture
def test_client(fresh_activities, monkeypatch):
    """Provide a TestClient with isolated activities data.
    
    Arrange: Monkeypatch the app's activities dict with a fresh copy
    for this test, ensuring complete isolation.
    """
    # Replace the app's activities dict with the fresh copy
    monkeypatch.setattr("src.app.activities", fresh_activities)
    return TestClient(app)


@pytest.fixture
def test_email():
    """Provide a test email address."""
    return "test@mergington.edu"


@pytest.fixture
def existing_email():
    """Provide an email that's already registered in activities."""
    return "michael@mergington.edu"  # Already in Chess Club
