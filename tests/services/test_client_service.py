import pytest

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import EmailUnavailableException, PhoneNumberUnavailableException
from tests.fixtures.client_fixture import client_obj, mock_db_repo, service, client_data

@pytest.mark.anyio
async def test_save_client(client_obj, mock_db_repo, service, client_data):
  mock_db_repo.get_by_email.return_value = None
  mock_db_repo.get_by_phone_number.return_value = None

  mock_db_repo.save.return_value = client_obj

  result = await service.save_client(client_data)

  assert result.first_name == client_data.first_name
  assert result.last_name == None
  assert result.email == client_data.email
  assert result.phone_number == client_data.phone_number
  assert result.notes == None
  assert mock_db_repo.save.call_count == 1

@pytest.mark.anyio
async def test_save_client_email_exception(mock_db_repo, service, client_data):
  mock_db_repo.get_by_email.return_value = EmailUnavailableException()

  with pytest.raises(EmailUnavailableException) as exc:
    await service.save_client(client_data)

  assert exc.value.status_code == 409
  assert f"Email '{client_data.email}' is already in use" in str(exc.value)

@pytest.mark.anyio
async def test_save_client_phone_number_exception(mock_db_repo, service, client_data):
  mock_db_repo.get_by_email.return_value = None
  mock_db_repo.get_by_phone_number.return_value = PhoneNumberUnavailableException()

  with pytest.raises(PhoneNumberUnavailableException) as exc:
    await service.save_client(client_data)

  assert exc.value.status_code == 409
  assert f"Phone number '{client_data.phone_number}' is already in use" in str(exc.value)

@pytest.mark.anyio
async def test_save_client_email_race_condition(mock_db_repo, service, client_data):
  mock_db_repo.get_by_email.return_value = None
  mock_db_repo.get_by_phone_number.return_value = None
  mock_db_repo.save.side_effect = IntegrityError("stmt", "params", "email")

  with pytest.raises(EmailUnavailableException) as exc:
    await service.save_client(client_data)

  assert exc.value.status_code == 409
  assert f"Email '{client_data.email}' is already in use" in str(exc.value)

@pytest.mark.anyio
async def test_save_client_phone_number_race_condition(mock_db_repo, service, client_data):
  mock_db_repo.get_by_email.return_value = None
  mock_db_repo.get_by_phone_number.return_value = None
  mock_db_repo.save.side_effect = IntegrityError("stmt", "params", "phone_number")

  with pytest.raises(PhoneNumberUnavailableException) as exc:
    await service.save_client(client_data)

  assert exc.value.status_code == 409
  assert f"Phone number '{client_data.phone_number}' is already in use" in str(exc.value)