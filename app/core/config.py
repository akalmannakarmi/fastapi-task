from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str
    REDIS_URL:str
    SECRET_KEY:str
    ALOGRITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 3 


    class Config():
        env_file=".env"

settings = Settings()
