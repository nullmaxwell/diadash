import pytest
from src.credentials.credentials import CredentialHandler


@pytest.fixture
def test_instantiation() -> None:
    """
    Fixture that initially sets the instantiation of the handler.
    """
    CredentialHandler.credential_loc = "tests/test_credentials.json"
    handler = CredentialHandler()
    # Resets the credentials back to the original path.
    CredentialHandler.credential_loc = "src/credentials/credentials.json"
    return handler


def test_getUser(test_instantiation) -> None:
    """
    Verifies that the getter functions work as intended
    """
    assert test_instantiation.getUser() == "TestUser", "User incorrect."


def test_getToken(test_instantiation) -> None:
    """
    Verifies that the getter functions work as intended
    """
    assert test_instantiation.getToken() == "TestPass", "Token incorrect."


def test_getNote(test_instantiation) -> None:
    """
    Verifies that the getter functions work as intended
    """
    assert test_instantiation.getNote() == "TestNote", "Note incorrect."
