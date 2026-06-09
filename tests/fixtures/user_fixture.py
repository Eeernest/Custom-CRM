from unittest.mock import AsyncMock, Mock

import pytest

from app.models.user_model import User
from app.repositories.user_db_repository import UserDbRepository
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService
from tests.conftest import db_session

@pytest.fixture()
def db_repo(db_session):
  return UserDbRepository(db_session)

@pytest.fixture()
def user_obj():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123"
  )

@pytest.fixture()
async def saved_user_obj(db_repo, user_obj):
  return await db_repo.save(user_obj)

@pytest.fixture()
def user_data():
  return UserCreate(
    username="user1",
    email="user1@example.com",
    password="Password123"
  )

@pytest.fixture()
def mock_security():
  return AsyncMock()

@pytest.fixture()
def mock_db_repo():
  return AsyncMock()

@pytest.fixture()
def service(mock_security, mock_db_repo):
  return UserService(mock_security, mock_db_repo)