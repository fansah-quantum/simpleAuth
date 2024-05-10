from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    version: str = "1.0"
    releaseId: str = "0.1"
    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "Simple Authentication Service"
    APP_DESCRIPTION: str = "Just a simple auth app"
    TESTING: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    JWT_ACCESS_TOKEN_EXPIRE: int = 30
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str 
    API_USER: str
    API_KEY: str
    
   

    class Config:
        env_file = ".env"
