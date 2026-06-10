from unittest.mock import AsyncMock

import pytest

from app.models.client_model import Client
from app.repositories.client_db_repository import ClientDbRepository
from app.schemas.client_schema import ClientCreate
from app.services.client_service import ClientService
from tests.conftest import db_session

@pytest.fixture()
def db_repo(db_session):
  return ClientDbRepository(db_session)

@pytest.fixture()
def client_obj():
  return Client(
    first_name="client",
    email="client@example.com",
    phone_number="111 111 111"
  )

@pytest.fixture()
async def saved_client_obj(db_repo, client_obj):
  return await db_repo.save(client_obj)

@pytest.fixture()
def mock_db_repo():
  return AsyncMock()

@pytest.fixture()
def service(mock_db_repo):
  return ClientService(mock_db_repo)

@pytest.fixture
def client_data():
  return ClientCreate(
    first_name="client",
    email="client@excample.com",
    phone_number="111 111 111"
  )