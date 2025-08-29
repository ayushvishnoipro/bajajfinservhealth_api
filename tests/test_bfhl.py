"""
Tests for the BFHL API endpoint.
Tests the exact examples from the specification.
"""
import pytest
from fastapi.testclient import TestClient
import os

# Set test environment variables
os.environ["FULL_NAME"] = "john_doe"
os.environ["DOB_DDMMYYYY"] = "17091999"
os.environ["EMAIL"] = "john@xyz.com"
os.environ["ROLL_NUMBER"] = "ABCD123"

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["user_id"] == "john_doe_17091999"


def test_example_a():
    """
    Test Example A from specification:
    Input: ["a","1","334","4","R", "$"]
    """
    request_data = {"data": ["a", "1", "334", "4", "R", "$"]}
    response = client.post("/bfhl", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert data["is_success"] is True
    assert data["user_id"] == "john_doe_17091999"
    assert data["email"] == "john@xyz.com"
    assert data["roll_number"] == "ABCD123"
    
    # Check categorized data
    assert data["odd_numbers"] == ["1"]
    assert data["even_numbers"] == ["334", "4"]
    assert data["alphabets"] == ["A", "R"]
    assert data["special_characters"] == ["$"]
    assert data["sum"] == "339"
    assert data["concat_string"] == "Ra"


def test_example_b():
    """
    Test Example B from specification:
    Input: ["2","a", "y", "4", "&", "-", "*", "5","92","b"]
    """
    request_data = {"data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]}
    response = client.post("/bfhl", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert data["is_success"] is True
    assert data["user_id"] == "john_doe_17091999"
    assert data["email"] == "john@xyz.com"
    assert data["roll_number"] == "ABCD123"
    
    # Check categorized data
    assert data["even_numbers"] == ["2", "4", "92"]
    assert data["odd_numbers"] == ["5"]
    assert data["alphabets"] == ["A", "Y", "B"]
    assert data["special_characters"] == ["&", "-", "*"]
    assert data["sum"] == "103"
    assert data["concat_string"] == "ByA"


def test_example_c():
    """
    Test Example C from specification:
    Input: ["A","ABcD","DOE"]
    """
    request_data = {"data": ["A", "ABcD", "DOE"]}
    response = client.post("/bfhl", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert data["is_success"] is True
    assert data["user_id"] == "john_doe_17091999"
    assert data["email"] == "john@xyz.com"
    assert data["roll_number"] == "ABCD123"
    
    # Check categorized data
    assert data["even_numbers"] == []
    assert data["odd_numbers"] == []
    assert data["alphabets"] == ["A", "ABCD", "DOE"]
    assert data["special_characters"] == []
    assert data["sum"] == "0"
    assert data["concat_string"] == "EoDdCbAa"


def test_empty_data():
    """Test with empty data array."""
    request_data = {"data": []}
    response = client.post("/bfhl", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["is_success"] is True
    assert data["odd_numbers"] == []
    assert data["even_numbers"] == []
    assert data["alphabets"] == []
    assert data["special_characters"] == []
    assert data["sum"] == "0"
    assert data["concat_string"] == ""


def test_mixed_types():
    """Test with mixed data types (numbers and strings)."""
    request_data = {"data": [1, "2", "abc", 3.5, "def"]}
    response = client.post("/bfhl", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["is_success"] is True
    # Numbers should be converted to strings and processed
    assert "1" in data["odd_numbers"]
    assert "2" in data["even_numbers"]
    assert "ABC" in data["alphabets"]
    assert "DEF" in data["alphabets"]
    assert "3.5" in data["special_characters"]  # Not pure digits


def test_invalid_request_structure():
    """Test with invalid request structure (missing data field)."""
    request_data = {"invalid": ["test"]}
    response = client.post("/bfhl", json=request_data)
    
    # Should return 422 for validation error (Pydantic validation)
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
