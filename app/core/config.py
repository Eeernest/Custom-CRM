from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
  POSTGRES_URL: str

  ADMIN_USERNAME: str

  ADMIN_EMAIL: str

  ADMIN_HASHED_PASSWORD: str

  DUMMY_HASH: str

  SECRET_KEY: str

  ALGORITHM: str

  ACCESS_TOKEN_EXPIRE_MINUTES: int
  
  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    case_sensitive=True
  )

settings = Config()