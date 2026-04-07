from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # This automatically looks for SUPERHERO_API_TOKEN in your .env
    superhero_api_token: str = ""

    # Tells Pydantic where to find the file
    model_config = SettingsConfigDict(env_file=".env")


# Create a single instance to be used everywhere
settings = Settings()
