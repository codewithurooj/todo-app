"""Unit tests for validator functions."""

import pytest
from src.utils.validators import validate_title, validate_description


class TestValidateTitle:
    """Tests for validate_title function."""

    def test_valid_title(self) -> None:
        """Valid title passes validation."""
        is_valid, error = validate_title("Buy groceries")
        assert is_valid is True
        assert error == ""

    def test_empty_title_rejected(self) -> None:
        """Empty string title fails validation."""
        is_valid, error = validate_title("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_whitespace_only_title_rejected(self) -> None:
        """Whitespace-only title fails validation."""
        is_valid, error = validate_title("   ")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_title_exactly_200_chars_accepted(self) -> None:
        """Boundary: 200 characters is valid."""
        title = "a" * 200
        is_valid, error = validate_title(title)
        assert is_valid is True
        assert error == ""

    def test_title_201_chars_rejected(self) -> None:
        """Boundary: 201 characters is invalid."""
        title = "a" * 201
        is_valid, error = validate_title(title)
        assert is_valid is False
        assert "201" in error
        assert "200" in error


class TestValidateDescription:
    """Tests for validate_description function."""

    def test_valid_description(self) -> None:
        """Valid description passes validation."""
        is_valid, error = validate_description("Get milk, bread, and eggs")
        assert is_valid is True
        assert error == ""

    def test_none_description_valid(self) -> None:
        """None description is valid (optional field)."""
        is_valid, error = validate_description(None)
        assert is_valid is True
        assert error == ""

    def test_empty_description_valid(self) -> None:
        """Empty string description is valid (optional field)."""
        is_valid, error = validate_description("")
        assert is_valid is True
        assert error == ""

    def test_description_exactly_1000_chars_accepted(self) -> None:
        """Boundary: 1000 characters is valid."""
        description = "a" * 1000
        is_valid, error = validate_description(description)
        assert is_valid is True
        assert error == ""

    def test_description_1001_chars_rejected(self) -> None:
        """Boundary: 1001 characters is invalid."""
        description = "a" * 1001
        is_valid, error = validate_description(description)
        assert is_valid is False
        assert "1001" in error
        assert "1000" in error
