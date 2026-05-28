"""
Shared validation helpers for backend Pydantic schemas.
"""

import re


class StringValidator:
    @staticmethod
    def validate_not_empty(value: str, field_name: str) -> str:
        if value is None:
            raise ValueError(f"{field_name} cannot be empty")

        cleaned = value.strip()
        if not cleaned:
            raise ValueError(f"{field_name} cannot be empty")

        return cleaned


class OTPValidator:
    @staticmethod
    def validate_numeric(value: str) -> str:
        if not value.isdigit():
            raise ValueError("OTP must contain only numbers")

        return value


class PasswordValidator:
    @staticmethod
    def validate_strength(value: str) -> str:
        if value is None:
            raise ValueError("Password cannot be empty")

        password = value.strip()
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")

        return password