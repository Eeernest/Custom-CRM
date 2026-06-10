import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import UsernameUnavailableException, EmailUnavailableException, PasswordTooShortException, PasswordNumberException, PasswordNoUppercaseException
from tests.fixtures.user_fixture import user_obj, user_data, mock_security, mock_db_repo, service

@pytest.mark.anyio
async def test_create_account_succsess(user_obj, user_data, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = None

  mock_security.get_password_hash.return_value = user_obj.hashed_password

  mock_db_repo.save.return_value = user_obj

  result = await service.create_account(user_data)

  assert result.username == user_data.username
  assert result.email == user_data.email
  assert mock_db_repo.save.call_count == 1

@pytest.mark.anyio
async def test_create_account_username_exception(user_obj, user_data, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = user_obj
  
  with pytest.raises(UsernameUnavailableException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 409
  assert f"Username '{user_data.username}' is already in use" in str(exc.value)

@pytest.mark.anyio
async def test_create_account_email_exception(user_obj, user_data, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = user_obj

  with pytest.raises(EmailUnavailableException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 409
  assert f"Email '{user_data.email}' is already in use" in str(exc.value)

@pytest.mark.anyio
async def test_create_account_password_too_short_exception(user_data, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = None

  mock_security.get_password_hash.side_effect = PasswordTooShortException()

  with pytest.raises(PasswordTooShortException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 422
  assert exc.value.detail == "Password should have at least 8 characters"

@pytest.mark.anyio
async def test_create_account_password_number_exception(user_data, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = None

  mock_security.get_password_hash.side_effect = PasswordNumberException()

  with pytest.raises(PasswordNumberException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 422
  assert exc.value.detail == "Password should have at least one number"

@pytest.mark.anyio
async def test_create_account_password_no_uppercase_exception(user_data, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = None

  mock_security.get_password_hash.side_effect = PasswordNoUppercaseException()

  with pytest.raises(PasswordNoUppercaseException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 422
  assert exc.value.detail == "Password should have at least one big letter"

@pytest.mark.anyio
async def test_create_account_username_race_condition_failure(user_obj, user_data, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = None

  mock_security.get_password_hash.return_value = user_obj.hashed_password

  mock_db_repo.save.side_effect = IntegrityError("stmt", "params", "username")

  with pytest.raises(UsernameUnavailableException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 409
  assert f"Username '{user_data.username}' is already in use" in str(exc.value)
  assert mock_db_repo.save.call_count == 1

@pytest.mark.anyio
async def test_create_account_email_race_condition_failure(user_obj, user_data, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_db_repo.get_by_email.return_value = None

  mock_security.get_password_hash.return_value = user_obj.hashed_password

  mock_db_repo.save.side_effect = IntegrityError("stmt", "params", "email")

  with pytest.raises(EmailUnavailableException) as exc:
    await service.create_account(user_data)

  assert exc.value.status_code == 409
  assert f"Email '{user_data.email}' is already in use" in str(exc.value)
  assert mock_db_repo.save.call_count == 1