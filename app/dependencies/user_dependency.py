from typing import Annotated

from fastapi import Depends

from app.core.security import Security
from app.db.database import SessionDep
from app.repositories.user_db_repository import UserDbRepository
from app.services.user_service import UserService

def get_user_service(session: SessionDep):
  security = Security()
  db_repo = UserDbRepository(session)

  return UserService(security, db_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]