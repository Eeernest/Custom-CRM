from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppBaseException, UsernameUnavailableException, EmailUnavailableException
from app.core.security import Security
from app.models.user_model import User
from app.repositories.user_db_repository import UserDbRepository
from app.schemas.user_schema import UserCreate

class UserService:
  def __init__(self, security: Security, db_repo: UserDbRepository):
    self.security = security
    self.db_repo = db_repo

  async def create_account(self, user_data: UserCreate) -> User:
    if await self.db_repo.get_by_username(user_data.username) is not None:
      raise UsernameUnavailableException(f"Username '{user_data.username}' is already in use")
    
    if await self.db_repo.get_by_email(user_data.email) is not None:
      raise EmailUnavailableException(f"Email '{user_data.email}' is already in use")
    
    hashed_password = await self.security.get_password_hash(user_data.password)

    user_obj = User(
      username=user_data.username,
      email=user_data.email,
      hashed_password=hashed_password
    )

    try:
      await self.db_repo.save(user_obj)
      
      return user_obj
    
    except IntegrityError as exc:
      if "username" in str(exc.orig):
        raise UsernameUnavailableException(f"Username '{user_data.username}' is already in use")
      
      if "email" in str(exc.orig):
        raise EmailUnavailableException(f"Email '{user_data.email}' is already in use")
      
    raise AppBaseException("failed to create account")