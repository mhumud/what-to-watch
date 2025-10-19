from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://streamuser:streampass@localhost:5432/streamdb"
    omdb_api_key: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
