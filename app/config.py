"""
Configuration module for the BFHL FastAPI application.
Handles environment variables and computes the user ID.
"""
import os
from typing import Optional


def get_env_var(name: str, default: Optional[str] = None) -> str:
    """Get environment variable with optional default value."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} is required")
    return value


# Environment variables
FULL_NAME = get_env_var("FULL_NAME", "john_doe")
DOB_DDMMYYYY = get_env_var("DOB_DDMMYYYY", "29082025")
EMAIL = get_env_var("EMAIL", "john@example.com")
ROLL_NUMBER = get_env_var("ROLL_NUMBER", "ABCD123")

# Computed user ID: full_name_ddmmyyyy (lowercased)
USER_ID = f"{FULL_NAME.lower()}_{DOB_DDMMYYYY}"
