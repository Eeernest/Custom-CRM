import pytest

from app.core.exceptions import EmailUnavailableException, PhoneNumberUnavailableException
from tests.fixtures.client_fixture import db_repo, client_obj, mock_service, mock_client, client_data_payload, integration_service, integration_client

@pytest.mark.anyio
async def test_save_client_success(client_obj, mock_service, mock_client, client_data_payload):
  client_obj.id = 1

  mock_service.save_client.return_value = client_obj

  result = await mock_client.post("/save", json=client_data_payload)
  data = result.json()

  assert result.status_code == 200
  assert data["first_name"] == client_obj.first_name
  assert data["email"] == client_obj.email
  assert data["phone_number"] == client_obj.phone_number

@pytest.mark.anyio
async def test_save_client_email_exception(mock_service, mock_client, client_data_payload):
  mock_service.save_client.side_effect = EmailUnavailableException()

  result = await mock_client.post("/save", json=client_data_payload)
  data = result.json()

  assert result.status_code == 409
  assert data["detail"] == "Email is already in use"

@pytest.mark.anyio
async def test_save_client_phone_number_exception(mock_service, mock_client, client_data_payload):
  mock_service.save_client.side_effect = PhoneNumberUnavailableException()

  result = await mock_client.post("/save", json=client_data_payload)
  data = result.json()

  assert result.status_code == 409
  assert data["detail"] == "Phone number is already in use"

@pytest.mark.anyio
async def test_integration_save_client(client_obj, client_data_payload, integration_client):
  result = await integration_client.post("/save", json=client_data_payload)
  data = result.json()

  assert result.status_code == 200
  assert data["first_name"] == client_obj.first_name