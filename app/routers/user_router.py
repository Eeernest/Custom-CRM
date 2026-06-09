from fastapi import APIRouter

from app.dependencies.user_dependency import UserServiceDep
from app.schemas.user_schema import UserCreate, UserRead

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(service: UserServiceDep, user_data: UserCreate):
  return await service.create_account(user_data)