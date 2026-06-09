import pytest

from app.core.exceptions import InvalidCredentialsException
from tests.fixtures.auth_fixture import user_obj, mock_security, mock_db_repo, service

@pytest.mark.anyio
async def test_login_success(user_obj, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = user_obj
  mock_security.verify_password.return_value = True
  mock_security.encode_jwt.return_value = "jwt_token"

  result = await service.login(user_obj.username, "Password123")

  assert result.access_token == "jwt_token"
  assert result.token_type == "bearer"

@pytest.mark.anyio
async def test_login_username_failure(mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = None
  mock_security.verify_password.return_value = False

  with pytest.raises(InvalidCredentialsException) as exc:
    await service.login("wrong_username", "Password123")

  assert exc.value.status_code == 401
  assert exc.value.detail == "Incorrect username or password"

@pytest.mark.anyio
async def test_login_password_failure(user_obj, mock_security, mock_db_repo, service):
  mock_db_repo.get_by_username.return_value = user_obj
  mock_security.verify_password.return_value = False

  with pytest.raises(InvalidCredentialsException) as exc:
    await service.login(user_obj.username, "Wrongpassword123")

  assert exc.value.status_code == 401
  assert exc.value.detail == "Incorrect username or password"