import pytest

from app.core.exceptions import InvalidCredentialsException
from tests.fixtures.auth_fixture import data_payload, token, mock_service, mock_client

@pytest.fixture()
async def test_login_success(data_payload, token, mock_service, mock_client):
  mock_service.login.return_value = token

  result = await mock_client.post("/token", data=data_payload)
  data = result.json()

  assert result.status_code == 200
  assert data["access_token"] == "fake_token"
  assert data["token_type"] == "bearer"

@pytest.fixture()
async def test_login_username_failure(mock_service, mock_client):
  mock_service.login.side_effect = InvalidCredentialsException

  result = await mock_client.post("/token", data={"username": "user2", "password": "Password123"})
  data = result.json()

  assert result.status_code == 401
  assert data["detail"] == "Invalid username or password"