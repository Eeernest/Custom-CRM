import pytest

from app.core.exceptions import UsernameUnavailableException, EmailUnavailableException
from tests.fixtures.user_fixture import user_obj, mock_service, user_data_payload, mock_client, integration_service, integration_client

@pytest.mark.anyio
async def test_register_success(user_obj, mock_service, user_data_payload, mock_client):
  user_obj.id = 1
  
  mock_service.create_account.return_value = user_obj

  result = await mock_client.post("/register", json=user_data_payload)
  data = result.json()

  assert result.status_code == 200
  assert data["username"] == user_obj.username
  assert data["email"] == user_obj.email
  assert mock_service.create_account.call_count == 1

@pytest.mark.anyio
async def test_register_username_failure(mock_service, user_data_payload, mock_client):
  mock_service.create_account.side_effect = UsernameUnavailableException

  result = await mock_client.post("/register", json=user_data_payload)
  data = result.json()

  assert result.status_code == 409
  assert data["detail"] == "Username is already in use"

@pytest.mark.anyio
async def test_register_email_failure(mock_service, user_data_payload, mock_client):
  mock_service.create_account.side_effect = EmailUnavailableException

  result = await mock_client.post("/register", json=user_data_payload)
  data = result.json()

  assert result.status_code == 409
  assert data["detail"] == "Email is already in use"

@pytest.mark.anyio
async def test_user_happy_path(user_obj, user_data_payload, integration_client):
  register_result = await integration_client.post("/register", json=user_data_payload)
  register_data = register_result.json()

  assert register_result.status_code == 200
  assert register_data["username"] == user_obj.username
  assert register_data["email"] == user_obj.email