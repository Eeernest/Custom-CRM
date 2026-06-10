import pytest

from tests.fixtures.client_fixture import db_repo, client_obj, saved_client_obj

@pytest.mark.anyio
async def test_save(db_repo, client_obj):
  result = await db_repo.save(client_obj)

  assert result.id is not None
  assert result.first_name == client_obj.first_name
  assert result.email == client_obj.email
  assert result.phone_number == client_obj.phone_number

@pytest.mark.anyio
async def test_get_by_email(db_repo, saved_client_obj):
  result = await db_repo.get_by_email(saved_client_obj.email)

  assert result.email == saved_client_obj.email

@pytest.mark.anyio
async def test_get_by_phone_number(db_repo, saved_client_obj):
  result = await db_repo.get_by_phone_number(saved_client_obj.phone_number)

  assert result.phone_number == saved_client_obj.phone_number