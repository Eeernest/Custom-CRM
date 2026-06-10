from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.core.security import Security
from app.dependencies.user_dependency import get_user_service
from app.main import app
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

@pytest.fixture()
def mock_service():
  return AsyncMock()

@pytest.fixture()
async def mock_client(mock_service):
  app.dependency_overrides[get_user_service] = lambda: mock_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()

@pytest.fixture()
def user_data_payload():
  return {
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123"
  }

@pytest.fixture()
def integration_service(db_session):
  security = Security()
  db_repo = UserDbRepository(db_session)

  return UserService(security, db_repo)

@pytest.fixture()
async def integration_client(integration_service):
  app.dependency_overrides[get_user_service] = lambda: integration_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()