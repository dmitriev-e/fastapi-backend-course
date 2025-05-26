from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME : str
    DB_USER : str
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : int
    
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()