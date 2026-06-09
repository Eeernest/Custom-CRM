import pytest

from app.models.user_model import User
from app.repositories.user_db_repository import UserDbRepository
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