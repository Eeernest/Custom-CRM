from pydantic import BaseModel, EmailStr, field_validator

class ClientBase(BaseModel):
  first_name: str
  last_name: str | None = None
  email: EmailStr
  phone_number: str

  @field_validator("email")
  def lowercase_email(cls, v: str) -> str:
    return v.lower().strip()
  
class ClientCreate(ClientBase):
  notes: str | None = None