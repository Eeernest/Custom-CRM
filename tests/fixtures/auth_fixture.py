from unittest.mock import AsyncMock

import pytest

from app.models.user_model import User
from app.services.auth_service import AuthService

@pytest.fixture()
def user_obj():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123"
  )

@pytest.fixture()
def mock_security():
  return AsyncMock()

@pytest.fixture()
def mock_db_repo():
  return AsyncMock()

@pytest.fixture()
def service(mock_security, mock_db_repo):
  return AuthService(mock_security, mock_db_repo)